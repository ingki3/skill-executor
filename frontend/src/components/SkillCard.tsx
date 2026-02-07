import React from 'react';
import { Card, CardContent, Typography, Button, Box, Chip } from '@mui/material';
import type { Skill } from '../services/api';
import SyncIcon from '@mui/icons-material/Sync';
import DeleteIcon from '@mui/icons-material/Delete';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';

interface SkillCardProps {
  skill: Skill;
  onSync: (id: string) => void;
  onDelete: (id: string) => void;
  onExecute: (skill: Skill) => void;
}

export const SkillCard: React.FC<SkillCardProps> = ({ skill, onSync, onDelete, onExecute }) => {
  return (
    <Card sx={{ minWidth: 275, mb: 2 }}>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
          <Typography variant="h5" component="div">
            {skill.name}
          </Typography>
          <Chip
            label={skill.complexity}
            color={skill.complexity === 'COMPLEX' ? 'secondary' : 'primary'}
            size="small"
          />
        </Box>
        <Typography sx={{ mb: 1.5 }} color="text.secondary">
          v{skill.version}
        </Typography>
        <Typography variant="body2" mb={2}>
          {skill.description}
        </Typography>
        <Box display="flex" gap={1}>
          <Button
            size="small"
            variant="contained"
            startIcon={<PlayArrowIcon />}
            onClick={() => onExecute(skill)}
          >
            Run
          </Button>
          <Button
            size="small"
            variant="outlined"
            startIcon={<SyncIcon />}
            onClick={() => onSync(skill.id)}
          >
            Sync
          </Button>
          <Button
            size="small"
            variant="outlined"
            color="error"
            startIcon={<DeleteIcon />}
            onClick={() => onDelete(skill.id)}
          >
            Delete
          </Button>
        </Box>
      </CardContent>
    </Card>
  );
};
