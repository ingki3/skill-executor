import React from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button,
  Chip,
  Typography,
  Box,
  CircularProgress
} from '@mui/material';
import type { RegistrationBatch, RegistrationQueueItem } from '../services/registration_api';

interface Props {
  batch: RegistrationBatch;
  onReview: (item: RegistrationQueueItem) => void;
  onApprove: (path: string) => void;
  onReject: (path: string) => void;
  onApproveAllSafe: () => void;
}

const RegistrationQueue: React.FC<Props> = ({
  batch,
  onReview,
  onApprove,
  onReject,
  onApproveAllSafe
}) => {
  return (
    <Box sx={{ mb: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h5">Registration Queue</Typography>
        <Box>
          <Button
            variant="outlined"
            color="success"
            onClick={onApproveAllSafe}
            disabled={batch.status === 'SCANNING'}
            sx={{ mr: 1 }}
          >
            Approve All Safe
          </Button>
        </Box>
      </Box>

      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }}>
          <TableHead>
            <TableRow>
              <TableCell>Skill Name</TableCell>
              <TableCell>Safety Status</TableCell>
              <TableCell>Judgment</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {batch.items.map((item) => (
              <TableRow key={item.path}>
                <TableCell>{item.name}</TableCell>
                                <TableCell>
                                  {item.safety_status === 'SCANNING' ? (
                                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                                      <CircularProgress size={16} />
                                      <Typography variant="body2">Scanning...</Typography>
                                    </Box>
                                  ) : item.safety_status === 'FAILED' ? (
                                    <Box>
                                      <Chip label="FAILED" color="error" size="small" />
                                      <Typography variant="caption" display="block" color="error">
                                        {item.error_message}
                                      </Typography>
                                    </Box>
                                  ) : (
                                    <Chip 
                                      label={item.safety_status} 
                                      color={item.safety_status === 'SAFE' ? 'success' : 'warning'} 
                                      size="small" 
                                    />
                                  )}
                                </TableCell>
                
                <TableCell>
                  <Chip
                    label={item.judgment}
                    variant="outlined"
                    size="small"
                  />
                </TableCell>
                <TableCell align="right">
                  <Button size="small" onClick={() => onReview(item)}>Review</Button>
                  <Button
                    size="small"
                    color="success"
                    onClick={() => onApprove(item.path)}
                    disabled={item.judgment !== 'PENDING' || item.safety_status === 'SCANNING'}
                  >
                    Approve
                  </Button>
                  <Button
                    size="small"
                    color="error"
                    onClick={() => onReject(item.path)}
                    disabled={item.judgment !== 'PENDING' || item.safety_status === 'SCANNING'}
                  >
                    Reject
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default RegistrationQueue;
