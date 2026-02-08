
export type ExecutionStatus = 'RUNNING' | 'PAUSED' | 'COMPLETED' | 'FAILED' | 'THINKING' | 'TOOL_CALL';

export interface ExecutionEvent {
  event: 'status_update' | 'request_input' | 'final_answer' | 'error';
  payload: any;
}

export interface StartExecutionRequest {
  skill_id: string;
  input: string;
  mode: 'HITL' | 'AUTONOMOUS';
  config?: {
    model_id?: string;
    max_steps?: number;
  };
}

export interface StartExecutionResponse {
  session_id: string;
  status: string;
}

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const WS_BASE_URL = API_BASE_URL.replace(/^http/, 'ws');

export const startExecution = async (request: StartExecutionRequest): Promise<StartExecutionResponse> => {
  const response = await fetch(`${API_BASE_URL}/execution/start`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error('Failed to start execution');
  }

  return response.json();
};

export const getSessionStatus = async (sessionId: string) => {
  const response = await fetch(`${API_BASE_URL}/execution/sessions/${sessionId}`);
  if (!response.ok) {
    throw new Error('Failed to fetch session status');
  }
  return response.json();
};

export class ExecutionStream {
  private socket: WebSocket | null = null;
  private sessionId: string;
  private onMessage: (event: ExecutionEvent) => void;
  private onError: (error: any) => void;
  private onOpen: () => void;
  private onClose: () => void;

  constructor(
    sessionId: string,
    onMessage: (event: ExecutionEvent) => void,
    onError: (error: any) => void,
    onOpen: () => void,
    onClose: () => void
  ) {
    this.sessionId = sessionId;
    this.onMessage = onMessage;
    this.onError = onError;
    this.onOpen = onOpen;
    this.onClose = onClose;
  }

  connect() {
    this.socket = new WebSocket(`${WS_BASE_URL}/execution/ws/${this.sessionId}`);

    this.socket.onopen = () => {
      this.onOpen();
    };

    this.socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data) as ExecutionEvent;
        this.onMessage(data);
      } catch (err) {
        console.error('Failed to parse WebSocket message', err);
        this.onError(err);
      }
    };

    this.socket.onerror = (error) => {
      console.error('WebSocket Error:', error);
      this.onError(error);
    };

    this.socket.onclose = (event) => {
      console.log('WebSocket Closed:', event.code, event.reason);
      this.onClose();
      
      // T024: Basic auto-reconnect if not closed normally
      if (event.code !== 1000 && event.code !== 1001) {
        setTimeout(() => {
          console.log('Attempting to reconnect...');
          this.connect();
        }, 3000);
      }
    };
  }

  sendResponse(content: string) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify({
        event: 'user_response',
        payload: { content }
      }));
    }
  }

  disconnect() {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }
}
