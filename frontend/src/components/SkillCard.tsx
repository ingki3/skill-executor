import React, { useState } from 'react';
import { Card, CardContent, Typography, Button, Box, Chip, CircularProgress, Dialog, DialogTitle, DialogContent, DialogActions, Divider } from '@mui/material';
import type { Skill } from '../services/api';
import { registrationApi } from '../services/registration_api';
import SyncIcon from '@mui/icons-material/Sync';
import DeleteIcon from '@mui/icons-material/Delete';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import DescriptionIcon from '@mui/icons-material/Description';
import ReactMarkdown from 'react-markdown';
import rehypeSanitize from 'rehype-sanitize';

interface SkillCardProps {
  skill: Skill;
  onSync: (id: string) => void;
  onDelete: (id: string) => void;
  onExecute: (skill: Skill) => void;
}

export const SkillCard: React.FC<SkillCardProps> = ({ skill, onSync, onDelete, onExecute }) => {
  const [docContent, setDocContent] = useState<string | null>(null);
  const [loadingDocs, setLoadingDocs] = useState(false);
  const [errorDocs, setErrorDocs] = useState<string | null>(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);

  const handleOpenDialog = () => {
    setIsDialogOpen(true);
    if (!docContent && !loadingDocs) {
      fetchDocs();
    }
  };

  const handleCloseDialog = () => {
    setIsDialogOpen(false);
  };

  const fetchDocs = async () => {
    setLoadingDocs(true);
    setErrorDocs(null);
    try {
      const response = await registrationApi.getSkillDocumentation(skill.id);
      setDocContent(response.data.content);
    } catch (err) {
      if (err && typeof err === 'object' && 'status' in err && (err as any).status === 404) {
        setDocContent(null);
        setErrorDocs("No documentation available.");
      } else {
        setErrorDocs("Failed to load documentation.");
      }
    } finally {
      setLoadingDocs(false);
    }
  };

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
          v{skill.version} • {skill.source_url.split('/').pop()}
        </Typography>
        <Typography variant="body2" mb={2}>
          {skill.description}
        </Typography>
        <Box display="flex" gap={1} mb={2}>
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
            startIcon={<DescriptionIcon />}
            onClick={handleOpenDialog}
          >
            View Skill
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

        <Dialog
          open={isDialogOpen}
          onClose={handleCloseDialog}
          fullWidth
          maxWidth="md"
          scroll="paper"
        >
          <DialogTitle>Skill Details</DialogTitle>
          <DialogContent dividers>
            <Box sx={{ mb: 3 }}>
              <Typography variant="body1" sx={{ color: 'black', mb: 1 }}>
                <strong>Name:</strong> {skill.name}
              </Typography>
              <Typography variant="body1" sx={{ color: 'black' }}>
                <strong>Description:</strong> {skill.description}
              </Typography>
            </Box>
            
            <Divider sx={{ mb: 3 }} />
            {loadingDocs ? (
              <Box display="flex" justifyContent="center" p={4}>
                <CircularProgress />
              </Box>
            ) : errorDocs ? (
              <Typography color="text.secondary" align="center" p={2}>
                {errorDocs}
              </Typography>
            ) : (
              <Box sx={{ color: 'black' }}>
                <article className="prose prose-slate max-w-none 
                  prose-headings:text-black 
                  prose-p:text-black 
                  prose-li:text-black 
                  prose-strong:text-black 
                  prose-code:text-black 
                  dark:prose-invert">
                  <ReactMarkdown rehypePlugins={[rehypeSanitize]}>
                    {docContent || ''}
                  </ReactMarkdown>
                </article>
              </Box>
            )}
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseDialog}>Close</Button>
          </DialogActions>
        </Dialog>
      </CardContent>
    </Card>
  );
};
