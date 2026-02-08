import React, { useState } from 'react';
import type { RepoSkill } from '../services/registration_api';
import {
  List,
  ListItem,
  ListItemText,
  Checkbox,
  Typography,
  Paper,
  Box
} from '@mui/material';

interface Props {
  skills: RepoSkill[];
  onSelectionChange: (selectedPaths: string[]) => void;
}

const SkillSelectionList: React.FC<Props> = ({ skills, onSelectionChange }) => {
  const [selected, setSelected] = useState<string[]>([]);

  const handleToggle = (path: string) => {
    const currentIndex = selected.indexOf(path);
    const newSelected = [...selected];

    if (currentIndex === -1) {
      newSelected.push(path);
    } else {
      newSelected.splice(currentIndex, 1);
    }

    setSelected(newSelected);
    onSelectionChange(newSelected);
  };

  if (skills.length === 0) {
    return <Typography color="textSecondary">No skills found in this repository.</Typography>;
  }

  return (
    <Box sx={{ mt: 2 }}>
      <Typography variant="h6" gutterBottom>
        Select Skills to Register
      </Typography>
      <Paper variant="outlined" sx={{ maxHeight: 300, overflow: 'auto' }}>
        <List>
          {skills.map((skill) => (
            <ListItem
              key={skill.path}
              dense
              component="div"
              onClick={() => handleToggle(skill.path)}
              sx={{ cursor: 'pointer' }}
            >
              <Checkbox
                edge="start"
                checked={selected.indexOf(skill.path) !== -1}
                tabIndex={-1}
                disableRipple
              />
              <ListItemText primary={skill.name} secondary={skill.path} />
            </ListItem>
          ))}
        </List>
      </Paper>
    </Box>
  );
};

export default SkillSelectionList;
