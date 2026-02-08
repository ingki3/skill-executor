
import React, { useEffect, useRef } from 'react';
import { Box, Paper, Typography, CircularProgress } from '@mui/material';
import ReactMarkdown from 'react-markdown';
import type { ExecutionEvent } from '../services/execution_api';

interface ExecutionMonitorProps {
  events: ExecutionEvent[];
  isThinking: boolean;
}

const ExecutionMonitor: React.FC<ExecutionMonitorProps> = ({ events, isThinking }) => {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [events, isThinking]);

  return (
    <Paper 
      elevation={3} 
      sx={{ 
        p: 2, 
        height: '500px', 
        overflowY: 'auto', 
        bgcolor: '#1e1e1e', 
        color: '#d4d4d4',
        fontFamily: 'monospace'
      }}
      ref={scrollRef}
    >
      <Typography variant="h6" gutterBottom sx={{ color: '#569cd6' }}>
        Execution Reasoning
      </Typography>
      
      {events.map((event, index) => (
        <Box key={index} sx={{ mb: 2, borderLeft: '2px solid #404040', pl: 2 }}>
          {event.event === 'status_update' && (
            <Box>
              <Typography variant="caption" sx={{ color: '#ce9178', fontWeight: 'bold' }}>
                [Thought]
              </Typography>
              <Box className="prose prose-invert max-w-none text-sm">
                <ReactMarkdown>{event.payload.thought}</ReactMarkdown>
              </Box>
              {event.payload.tool_call && (
                <Typography variant="body2" sx={{ color: '#4ec9b0', fontWeight: 'bold', mt: 1 }}>
                  Action: {event.payload.tool_call}
                </Typography>
              )}
            </Box>
          )}
          {event.event === 'request_input' && (
            <Box sx={{ 
              bgcolor: event.payload.role === 'HUMAN' ? 'rgba(78, 201, 176, 0.05)' : 'rgba(86, 156, 214, 0.1)', 
              p: 1.5, 
              borderRadius: 1,
              border: '1px solid',
              borderColor: event.payload.role === 'HUMAN' ? 'rgba(78, 201, 176, 0.2)' : 'rgba(86, 156, 214, 0.2)'
            }}>
              <Typography variant="body2" sx={{ 
                color: event.payload.role === 'HUMAN' ? '#4ec9b0' : '#569cd6', 
                fontWeight: 'bold',
                mb: 0.5
              }}>
                {event.payload.role === 'HUMAN' ? 'User:' : 'Agent:'}
              </Typography>
              <Box className="prose prose-invert max-w-none text-sm">
                <ReactMarkdown>{event.payload.prompt}</ReactMarkdown>
              </Box>
            </Box>
          )}
          {event.event === 'final_answer' && (
            <Box sx={{ mt: 3, p: 2, bgcolor: 'rgba(78, 201, 176, 0.1)', borderRadius: 1, border: '1px solid #4ec9b0' }}>
              <Typography variant="h6" sx={{ color: '#4ec9b0', mb: 1 }}>
                Final Answer
              </Typography>
              <Box className="prose prose-invert max-w-none">
                <ReactMarkdown>{event.payload.content}</ReactMarkdown>
              </Box>
            </Box>
          )}
          {event.event === 'error' && (
            <Typography variant="body2" sx={{ color: '#f44336', bgcolor: 'rgba(244, 67, 54, 0.1)', p: 1, borderRadius: 1 }}>
              Error: {event.payload.message}
            </Typography>
          )}
        </Box>
      ))}

      {isThinking && (
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 1 }}>
          <CircularProgress size={16} sx={{ color: '#569cd6' }} />
          <Typography variant="caption" sx={{ fontStyle: 'italic' }}>
            Agent is thinking...
          </Typography>
        </Box>
      )}
    </Paper>
  );
};

export default ExecutionMonitor;
