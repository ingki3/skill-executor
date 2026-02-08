import React from 'react';
import {
  Drawer,
  Box,
  Typography,
  Divider,
  List,
  ListItem,
  ListItemText,
  Chip,
  IconButton,
  Button
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import type { RegistrationQueueItem } from '../services/registration_api';

interface Props {
  item: RegistrationQueueItem | null;
  onClose: () => void;
  onApprove: (path: string) => void;
  onReject: (path: string) => void;
}

import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

const RiskDetailsPanel: React.FC<Props> = ({ item, onClose, onApprove, onReject }) => {
  if (!item) return null;

  return (
    <Drawer anchor="right" open={!!item} onClose={onClose}>
      <Box sx={{ width: 600, p: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h6">Skill Review: {item.name}</Typography>
          <IconButton onClick={onClose}><CloseIcon /></IconButton>
        </Box>

        <Divider sx={{ mb: 2 }} />

        <Typography variant="subtitle1" gutterBottom fontWeight="bold">
          Safety Status:
          <Chip
            label={item.safety_status}
            color={item.safety_status === 'SAFE' ? 'success' : 'warning'}
            size="small"
            sx={{ ml: 1 }}
          />
        </Typography>

        {item.risk_findings.length > 0 && (
          <Box sx={{ mb: 3 }}>
            <Typography variant="subtitle1" color="error" gutterBottom fontWeight="bold">
              Risk Findings:
            </Typography>
            <List dense>
              {item.risk_findings.map((finding, idx) => (
                <ListItem key={idx}>
                  <ListItemText
                    primary={`${finding.category} - ${finding.severity}`}
                    secondary={finding.detail}
                  />
                </ListItem>
              ))}
            </List>
          </Box>
        )}

        <Typography variant="subtitle1" gutterBottom fontWeight="bold">
          Source Code Preview:
        </Typography>
        <Box sx={{
          maxHeight: 500,
          overflow: 'auto',
          mb: 3,
          fontSize: '12px'
        }}>
          <SyntaxHighlighter
            language="python"
            style={vscDarkPlus}
            customStyle={{ margin: 0 }}
          >
            {item.code_content || '# No code preview available.'}
          </SyntaxHighlighter>
        </Box>

        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button
            fullWidth
            variant="contained"
            color="success"
            onClick={() => {
              onApprove(item.path);
              onClose();
            }}
            disabled={item.judgment !== 'PENDING'}
          >
            Approve
          </Button>
          <Button
            fullWidth
            variant="contained"
            color="error"
            onClick={() => {
              onReject(item.path);
              onClose();
            }}
            disabled={item.judgment !== 'PENDING'}
          >
            Reject
          </Button>
        </Box>
      </Box>
    </Drawer>
  );
};

export default RiskDetailsPanel;
