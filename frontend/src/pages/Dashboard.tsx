import React, { useEffect, useState } from 'react';
import { Container, Typography, Grid, Box, Button, TextField, Alert, CircularProgress } from '@mui/material';
import { skillApi, type Skill } from '../services/api';
import { SkillCard } from '../components/SkillCard';
import AddIcon from '@mui/icons-material/Add';

export const Dashboard: React.FC = () => {
  const [skills, setSkills] = useState<Skill[]>([]);
  const [loading, setLoading] = useState(true);
  const [registerUrl, setRegisterUrl] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [registering, setRegistering] = useState(false);

  const fetchSkills = async () => {
    try {
      const response = await skillApi.listSkills();
      setSkills(response.data);
    } catch (err) {
      setError('Failed to fetch skills');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSkills();
  }, []);

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!registerUrl) return;

    setRegistering(true);
    setError(null);
    try {
      await skillApi.registerSkill(registerUrl);
      setRegisterUrl('');
      fetchSkills();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Registration failed');
    } finally {
      setRegistering(false);
    }
  };

  const handleSync = async (id: string) => {
    try {
      await skillApi.syncSkill(id);
      fetchSkills();
    } catch (err) {
      setError('Sync failed');
    }
  };

  const handleDelete = async (id: string) => {
    if (window.confirm('Are you sure you want to delete this skill?')) {
      try {
        await skillApi.deleteSkill(id);
        fetchSkills();
      } catch (err) {
        setError('Delete failed');
      }
    }
  };

  const handleExecute = (skill: Skill) => {
    // Navigate to execution or show a modal
    alert(`Execute ${skill.name}`);
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>
        Skill Management Dashboard
      </Typography>

      <Box component="form" onSubmit={handleRegister} sx={{ mb: 4, display: 'flex', gap: 2 }}>
        <TextField
          label="GitHub Repo URL"
          variant="outlined"
          fullWidth
          value={registerUrl}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setRegisterUrl(e.target.value)}
          disabled={registering}
        />
        <Button
          type="submit"
          variant="contained"
          startIcon={registering ? <CircularProgress size={20} color="inherit" /> : <AddIcon />}
          disabled={registering || !registerUrl}
          sx={{ minWidth: '150px' }}
        >
          {registering ? 'Registering...' : 'Add Skill'}
        </Button>
      </Box>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      {loading ? (
        <Box display="flex" justifyContent="center">
          <CircularProgress />
        </Box>
      ) : (
        <Grid container spacing={3}>
          {skills.map((skill) => (
            <Grid size={{ xs: 12, sm: 6, md: 4 }} key={skill.id}>
              <SkillCard
                skill={skill}
                onSync={handleSync}
                onDelete={handleDelete}
                onExecute={handleExecute}
              />
            </Grid>
          ))}
          {skills.length === 0 && (
            <Grid size={{ xs: 12 }}>
              <Typography variant="body1" textAlign="center" color="text.secondary">
                No skills registered yet.
              </Typography>
            </Grid>
          )}
        </Grid>
      )}
    </Container>
  );
};
