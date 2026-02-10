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
  Chip,
  FormControlLabel,
  Switch
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { type Skill, type ExecutionLog } from '../services/api';
import { startExecution } from '../services/execution_api';

interface Props {
  skill: Skill | null;
  onClose: () => void;
}

const ExecutionDialog: React.FC<Props> = ({ skill, onClose }) => {
  const navigate = useNavigate();
  const [query, setQuery] = useState('');
  const [executing, setExecuting] = useState(false);
  const [hitlEnabled, setHitlEnabled] = useState(true);
  const [result, setResult] = useState<ExecutionLog | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleRun = async () => {
    if (!query || !skill) return;
    setExecuting(true);
    setError(null);
    setResult(null);
    try {
      const response = await startExecution({
        skill_id: skill.id,
        input: query,
        mode: hitlEnabled ? 'HITL' : 'AUTONOMOUS'
      });
      
      // Redirect to the execution dashboard for the new session
      navigate(`/execution/${response.session_id}`);
      onClose();
    } catch (err: any) {
      setError(err.message || 'Execution failed');
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
          <FormControlLabel
            control={
              <Switch 
                checked={hitlEnabled} 
                onChange={(e) => setHitlEnabled(e.target.checked)} 
                disabled={executing}
              />
            }
            label="Human-in-the-Loop (HITL) Mode"
            sx={{ mt: 1 }}
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
