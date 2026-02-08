import React, { useState } from 'react';
import { 
  Dialog, 
  DialogTitle, 
  DialogContent, 
  DialogActions, 
  Button, 
  TextField, 
  Box, 
  Typography, 
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  Divider,
  Chip
} from '@mui/material';
import { skillApi, type Skill, type ExecutionLog } from '../services/api';

interface Props {
  skill: Skill | null;
  onClose: () => void;
}

const ExecutionDialog: React.FC<Props> = ({ skill, onClose }) => {
  const [query, setQuery] = useState('');
  const [executing, setExecuting] = useState(false);
  const [result, setResult] = useState<ExecutionLog | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleRun = async () => {
    if (!query) return;
    setExecuting(true);
    setError(null);
    setResult(null);
    try {
      const response = await skillApi.executeSkill(query);
      setResult(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Execution failed');
    } finally {
      setExecuting(false);
    }
  };

  return (
    <Dialog open={!!skill} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>Execute Skill: {skill?.name}</DialogTitle>
      <DialogContent>
        <Box sx={{ mt: 1, mb: 3 }}>
          <TextField
            label="Enter your query or task"
            variant="outlined"
            fullWidth
            multiline
            rows={2}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={executing}
            placeholder="e.g., Check my unread emails"
          />
        </Box>

        {executing && (
          <Box display="flex" flexDirection="column" alignItems="center" my={4}>
            <CircularProgress />
            <Typography variant="body2" sx={{ mt: 2 }}>Agent is thinking...</Typography>
          </Box>
        )}

        {error && (
          <Typography color="error" variant="body2" sx={{ mb: 2 }}>
            {error}
          </Typography>
        )}

        {result && (
          <Box>
            <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
              <Typography variant="h6">Execution Results</Typography>
              <Chip 
                label={result.outcome} 
                color={result.outcome === 'SUCCESS' ? 'success' : 'error'} 
              />
            </Box>
            
            <Typography variant="subtitle2" gutterBottom>Steps:</Typography>
            <List dense>
              {result.steps.map((step, idx) => (
                <React.Fragment key={idx}>
                  <ListItem alignItems="flex-start">
                    <ListItemText
                      primary={`Step ${idx + 1}: ${step.thought}`}
                      secondary={step.observation && `Observation: ${step.observation}`}
                    />
                  </ListItem>
                  {idx < result.steps.length - 1 && <Divider component="li" />}
                </React.Fragment>
              ))}
            </List>

            <Box sx={{ mt: 2, display: 'flex', gap: 2 }}>
              <Typography variant="caption" color="text.secondary">
                Model: {result.model_used}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                Duration: {result.duration.toFixed(2)}s
              </Typography>
            </Box>
          </Box>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} disabled={executing}>Close</Button>
        <Button 
          onClick={handleRun} 
          variant="contained" 
          disabled={executing || !query}
        >
          {executing ? 'Executing...' : 'Run Skill'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default ExecutionDialog;
