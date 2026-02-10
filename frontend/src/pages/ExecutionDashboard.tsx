
import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Container, Typography, Box, Breadcrumbs, Link, Chip, Alert } from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import { 
  ExecutionStream, 
  getSessionStatus,
} from '../services/execution_api';
import type { 
  ExecutionEvent, 
  ExecutionStatus as ExecutionStatusType
} from '../services/execution_api';
import ExecutionMonitor from '../components/ExecutionMonitor';
import InputPrompt from '../components/InputPrompt';

const ExecutionDashboard: React.FC = () => {
  const { sessionId } = useParams<{ sessionId: string }>();
  const navigate = useNavigate();
  
  const [events, setEvents] = useState<ExecutionEvent[]>([]);
  const [status, setStatus] = useState<ExecutionStatusType>('RUNNING');
  const [isThinking, setIsThinking] = useState(false);
  const [inputRequest, setInputRequest] = useState<string | null>(null);
  const [stream, setStream] = useState<ExecutionStream | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleMessage = useCallback((event: ExecutionEvent) => {
    // Add role metadata to the event for UI labeling
    const enrichedEvent = { ...event };
    if (event.event === 'request_input') {
      (enrichedEvent.payload as any).role = 'AI';
    }
    setEvents(prev => [...prev, enrichedEvent]);
    
    if (event.event === 'status_update') {
      setStatus(event.payload.status as ExecutionStatusType);
      setIsThinking(event.payload.status === 'THINKING' || event.payload.status === 'TOOL_CALL');
    } else if (event.event === 'request_input') {
      setStatus('PAUSED');
      setIsThinking(false);
      setInputRequest(event.payload.prompt);
    } else if (event.event === 'final_answer') {
      setStatus('COMPLETED');
      setIsThinking(false);
      setInputRequest(null);
    } else if (event.event === 'error') {
      setStatus('FAILED');
      setIsThinking(false);
      setError(event.payload.message);
    }
  }, []);

  useEffect(() => {
    if (!sessionId) return;

    // Load initial history
    getSessionStatus(sessionId)
      .then(session => {
        setStatus(session.status);
        // Map history to events with explicit roles
        const historyEvents: ExecutionEvent[] = session.history.map((msg: any) => ({
          event: msg.role === 'AI' ? 'status_update' : 'request_input',
          payload: { 
            status: msg.role === 'AI' ? 'COMPLETED' : 'PAUSED',
            content: msg.content,
            prompt: msg.role === 'HUMAN' ? msg.content : undefined,
            role: msg.role // Preserving original role (AI or HUMAN)
          }
        }));
        setEvents(historyEvents);
      })
      .catch(() => setError('Failed to load session details'));

    const newStream = new ExecutionStream(
      sessionId,
      handleMessage,
      () => setError('WebSocket Connection Error'),
      () => console.log('Connected to stream'),
      () => console.log('Disconnected from stream')
    );

    newStream.connect();
    setStream(newStream);

    return () => {
      newStream.disconnect();
    };
  }, [sessionId, handleMessage]);

  const handleSendResponse = (content: string) => {
    if (stream) {
      stream.sendResponse(content);
      // Optimistically add to events with 'HUMAN' role
      setEvents(prev => [...prev, {
        event: 'request_input',
        payload: { 
          prompt: content,
          role: 'HUMAN' 
        }
      }]);
      setInputRequest(null);
      setIsThinking(true);
      setStatus('RUNNING');
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Breadcrumbs sx={{ mb: 2 }}>
        <Link 
          component="button" 
          variant="body2" 
          onClick={() => navigate('/')}
          sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}
        >
          <ArrowBackIcon fontSize="inherit" /> Dashboard
        </Link>
        <Typography color="text.primary">Execution: {sessionId?.substring(0, 8)}...</Typography>
      </Breadcrumbs>

      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Skill Execution
        </Typography>
        <Chip 
          label={status} 
          color={
            status === 'COMPLETED' ? 'success' : 
            status === 'FAILED' ? 'error' : 
            status === 'PAUSED' ? 'warning' : 'primary'
          } 
        />
      </Box>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      <ExecutionMonitor events={events} isThinking={isThinking} />

      <InputPrompt 
        onSend={handleSendResponse} 
        disabled={status !== 'PAUSED'} 
        prompt={inputRequest || undefined}
      />
    </Container>
  );
};

export default ExecutionDashboard;
