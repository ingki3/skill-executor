
import React, { useState } from 'react';
import { Box, TextField, Button, Paper, Typography } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';

interface InputPromptProps {
  onSend: (content: string) => void;
  disabled: boolean;
  prompt?: string;
}

const InputPrompt: React.FC<InputPromptProps> = ({ onSend, disabled, prompt }) => {
  const [value, setValue] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (value.trim() && !disabled) {
      onSend(value.trim());
      setValue('');
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 2, mt: 2 }}>
      {prompt && (
        <Typography variant="body2" color="primary" sx={{ mb: 1, fontWeight: 'bold' }}>
          {prompt}
        </Typography>
      )}
      <Box component="form" onSubmit={handleSubmit} sx={{ display: 'flex', gap: 1 }}>
        <TextField
          fullWidth
          size="small"
          placeholder={disabled ? "Waiting for agent..." : "Type your response here..."}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          disabled={disabled}
          autoFocus={!disabled}
        />
        <Button 
          variant="contained" 
          type="submit" 
          disabled={disabled || !value.trim()}
          endIcon={<SendIcon />}
        >
          Send
        </Button>
      </Box>
    </Paper>
  );
};

export default InputPrompt;
