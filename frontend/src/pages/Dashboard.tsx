import React, { useEffect, useState } from 'react';
import { 
  Container, 
  Typography, 
  Grid, 
  Box, 
  Button, 
  TextField, 
  Alert, 
  CircularProgress, 
  Snackbar,
  ToggleButton,
  ToggleButtonGroup,
  Tooltip
} from '@mui/material';
import { skillApi, type Skill } from '../services/api';
import { registrationApi, type RepoSkill, type RegistrationBatch, type RegistrationQueueItem } from '../services/registration_api';
import { SkillCard } from '../components/SkillCard';
import SkillSelectionList from '../components/SkillSelectionList';
import RegistrationQueue from '../components/RegistrationQueue';
import RiskDetailsPanel from '../components/RiskDetailsPanel';
import ExecutionDialog from '../components/ExecutionDialog';
import AddIcon from '@mui/icons-material/Add';
import SearchIcon from '@mui/icons-material/Search';
import GitHubIcon from '@mui/icons-material/GitHub';
import FolderIcon from '@mui/icons-material/Folder';
import { 
  Dialog, 
  DialogTitle, 
  DialogContent, 
  DialogContentText, 
  DialogActions 
} from '@mui/material';

export const Dashboard: React.FC = () => {
  const [skills, setSkills] = useState<Skill[]>([]);
  const [loading, setLoading] = useState(true);
  const [registerUrl, setRegisterUrl] = useState('');
  const [searchMode, setSearchMode] = useState<'github' | 'local'>('github');
  const [error, setError] = useState<string | null>(null);
  const [registering, setRegistering] = useState(false);
  const [repoSkills, setRepoSkills] = useState<RepoSkill[]>([]);
  const [listingSkills, setListingSkills] = useState(false);
  const [selectedPaths, setSelectedPaths] = useState<string[]>([]);
  
  // Deep link parsing state
  const [isDeepLink, setIsDeepLink] = useState(false);

  // Queue & Execution state
  const [activeBatch, setActiveBatch] = useState<RegistrationBatch | null>(null);
  const [reviewItem, setReviewItem] = useState<RegistrationQueueItem | null>(null);
  const [executingSkill, setExecutingSkill] = useState<Skill | null>(null);

  // Duplicate confirmation state
  const [confirmDialogOpen, setConfirmDialogOpen] = useState(false);
  const [duplicatePath, setDuplicatePath] = useState<string | null>(null);

  // Notification state
  const [snackbar, setSnackbar] = useState<{ open: boolean; message: string; severity: 'success' | 'error' }>({
    open: false,
    message: '',
    severity: 'success'
  });

  const showMessage = (message: string, severity: 'success' | 'error' = 'success') => {
    setSnackbar({ open: true, message, severity });
  };

  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };

  const handleSearchMode = (_: any, nextMode: 'github' | 'local') => {
    if (nextMode !== null) {
      setSearchMode(nextMode);
      setRepoSkills([]);
      setRegisterUrl('');
      setError(null);
      setIsDeepLink(false);
    }
  };

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

  const fetchPendingBatches = async () => {
    try {
      const response = await registrationApi.listBatches();
      const pending = response.data
        .filter(b => b.status === 'SCANNING' || b.status === 'REVIEW_REQUIRED')
        .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
      
      if (pending.length > 0) {
        setActiveBatch(pending[0]);
      }
    } catch (err) {
      console.error('Failed to fetch pending batches', err);
    }
  };

  useEffect(() => {
    fetchSkills();
    fetchPendingBatches();
  }, []);

  // Auto-detect deep link on input change
  useEffect(() => {
    const detectDeepLink = async () => {
      if (searchMode === 'github' && registerUrl.startsWith('http')) {
        try {
          const response = await registrationApi.parseGitHubUrl(registerUrl);
          setIsDeepLink(response.data.is_deep_link);
        } catch {
          setIsDeepLink(false);
        }
      } else {
        setIsDeepLink(false);
      }
    };
    
    const timer = setTimeout(detectDeepLink, 500);
    return () => clearTimeout(timer);
  }, [registerUrl, searchMode]);

  // Polling for batch status
  useEffect(() => {
    let timer: number;
    if (activeBatch && (activeBatch.status === 'SCANNING' || activeBatch.status === 'REVIEW_REQUIRED')) {
      timer = window.setInterval(async () => {
        try {
          const response = await registrationApi.getBatchStatus(activeBatch.id);
          setActiveBatch(response.data);
          if (response.data.status === 'COMPLETED') {
            setActiveBatch(null);
            fetchSkills();
            showMessage('Bulk registration completed successfully!');
          }
        } catch (err) {
          console.error('Polling failed', err);
          if ((err as any).response?.status === 404) {
            setActiveBatch(null);
            clearInterval(timer);
          }
        }
      }, 2000);
    }
    return () => clearInterval(timer);
  }, [activeBatch]);

  const handleListRepo = async () => {
    if (!registerUrl) return;
    
    // If it's a deep link, we go straight to scanning
    if (isDeepLink) {
      handleStartScanFromDeepLink();
      return;
    }

    setListingSkills(true);
    setRepoSkills([]);
    setError(null);
    try {
      if (searchMode === 'github') {
        const response = await registrationApi.listRepoSkills(registerUrl);
        setRepoSkills(response.data.skills);
      } else {
        const response = await registrationApi.listLocalSkills(registerUrl);
        setRepoSkills(response.data.skills.map(s => ({
          name: `${s.name}${s.has_metadata ? '' : ' (No metadata)'}`,
          path: s.path
        })));
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || `Failed to list skills from ${searchMode}`);
    } finally {
      setListingSkills(false);
    }
  };

  const handleStartScanFromDeepLink = async () => {
    setRegistering(true);
    setError(null);
    try {
      const response = await registrationApi.parseGitHubUrl(registerUrl);
      const { repo_url, sub_path } = response.data;
      
      if (!sub_path) {
        throw new Error('Could not identify a specific skill folder in this URL.');
      }

      const scanResponse = await registrationApi.startBatchScan(repo_url, [sub_path]);
      const batchResp = await registrationApi.getBatchStatus(scanResponse.data.batch_id);
      setActiveBatch(batchResp.data);
      setRegisterUrl('');
      setIsDeepLink(false);
      showMessage('Direct registration started...');
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || err.message || 'Failed to start direct registration';
      setError(errorMsg);
      showMessage(errorMsg, 'error');
    } finally {
      setRegistering(false);
    }
  };

  const handleStartScan = async () => {
    if (selectedPaths.length === 0) return;
    setRegistering(true);
    setError(null);
    try {
      const response = await registrationApi.startBatchScan(registerUrl, selectedPaths);
      const batchResp = await registrationApi.getBatchStatus(response.data.batch_id);
      setActiveBatch(batchResp.data);
      setRegisterUrl('');
      setRepoSkills([]);
      setSelectedPaths([]);
      showMessage('Batch scan started...');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to start scan');
    } finally {
      setRegistering(false);
    }
  };

  const handleApprove = async (path: string) => {
    if (!activeBatch) return;
    
    // Check if skill already exists
    const skillName = path.split('/').pop();
    const duplicate = skills.find(s => s.name === skillName);
    
    if (duplicate) {
      setDuplicatePath(path);
      setConfirmDialogOpen(true);
      return;
    }

    await performApprove(path);
  };

  const performApprove = async (path: string) => {
    if (!activeBatch) return;
    try {
      await registrationApi.judgeItem(activeBatch.id, path, 'APPROVED');
      const response = await registrationApi.getBatchStatus(activeBatch.id);
      setActiveBatch(response.data);
      showMessage(`Approved: ${path.split('/').pop()}`);
    } catch (err) {
      showMessage('Approval failed', 'error');
    }
  };

  const handleConfirmApprove = async () => {
    if (duplicatePath) {
      await performApprove(duplicatePath);
      setConfirmDialogOpen(false);
      setDuplicatePath(null);
    }
  };

  const handleReject = async (path: string) => {
    if (!activeBatch) return;
    try {
      await registrationApi.judgeItem(activeBatch.id, path, 'REJECTED');
      const response = await registrationApi.getBatchStatus(activeBatch.id);
      setActiveBatch(response.data);
      showMessage(`Rejected: ${path.split('/').pop()}`);
    } catch (err) {
      showMessage('Rejection failed', 'error');
    }
  };

  const handleApproveAllSafe = async () => {
    if (!activeBatch) return;
    try {
      const resp = await registrationApi.approveAllSafe(activeBatch.id);
      const response = await registrationApi.getBatchStatus(activeBatch.id);
      setActiveBatch(response.data);
      showMessage(`Approved ${resp.data.approved_count} safe skills.`);
    } catch (err) {
      showMessage('Bulk approval failed', 'error');
    }
  };

  const handleSync = async (id: string) => {
    try {
      await skillApi.syncSkill(id);
      fetchSkills();
      showMessage('Skill synced successfully');
    } catch (err) {
      showMessage('Sync failed', 'error');
    }
  };

  const handleDelete = async (id: string) => {
    if (window.confirm('Are you sure you want to delete this skill?')) {
      try {
        await skillApi.deleteSkill(id);
        fetchSkills();
        showMessage('Skill deleted');
      } catch (err) {
        showMessage('Delete failed', 'error');
      }
    }
  };

  const handleExecute = (skill: Skill) => {
    setExecutingSkill(skill);
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>
        Skill Management Dashboard
      </Typography>

      <Box sx={{ mb: 4 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
          <ToggleButtonGroup
            value={searchMode}
            exclusive
            onChange={handleSearchMode}
            size="small"
          >
            <ToggleButton value="github">
              <GitHubIcon sx={{ mr: 1 }} /> GitHub
            </ToggleButton>
            <ToggleButton value="local">
              <FolderIcon sx={{ mr: 1 }} /> Local
            </ToggleButton>
          </ToggleButtonGroup>
          
          <Tooltip title={searchMode === 'github' ? "GitHub Repo or Folder URL" : "Absolute server path within project root"}>
            <TextField
              label={searchMode === 'github' ? "GitHub URL" : "Local Directory Path"}
              variant="outlined"
              fullWidth
              value={registerUrl}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => setRegisterUrl(e.target.value)}
              disabled={registering || listingSkills}
              placeholder={searchMode === 'github' ? "https://github.com/..." : "/app/.skills/..."}
            />
          </Tooltip>
          
          <Button
            variant={isDeepLink ? "contained" : "outlined"}
            color={isDeepLink ? "primary" : "inherit"}
            onClick={handleListRepo}
            startIcon={listingSkills || registering ? <CircularProgress size={20} /> : (isDeepLink ? <AddIcon /> : <SearchIcon />)}
            disabled={registering || listingSkills || !registerUrl}
            sx={{ minWidth: '150px' }}
          >
            {listingSkills ? 'Searching...' : (registering ? 'Registering...' : (isDeepLink ? 'Register Direct' : 'Search'))}
          </Button>
          
          {!isDeepLink && (
            <Button
              variant="contained"
              onClick={handleStartScan}
              startIcon={registering ? <CircularProgress size={20} color="inherit" /> : <AddIcon />}
              disabled={registering || listingSkills || selectedPaths.length === 0}
              sx={{ minWidth: '150px' }}
            >
              {registering ? 'Scanning...' : 'Scan Selected'}
            </Button>
          )}
        </Box>

        {repoSkills.length > 0 && (
          <SkillSelectionList 
            skills={repoSkills} 
            onSelectionChange={setSelectedPaths} 
          />
        )}
      </Box>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      {activeBatch && (
        <RegistrationQueue 
          batch={activeBatch}
          onReview={setReviewItem}
          onApprove={handleApprove}
          onReject={handleReject}
          onApproveAllSafe={handleApproveAllSafe}
        />
      )}

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

      <RiskDetailsPanel 
        item={reviewItem}
        onClose={() => setReviewItem(null)}
        onApprove={handleApprove}
        onReject={handleReject}
      />

      <ExecutionDialog 
        skill={executingSkill}
        onClose={() => setExecutingSkill(null)}
      />

      {/* Duplicate Confirmation Dialog */}
      <Dialog
        open={confirmDialogOpen}
        onClose={() => setConfirmDialogOpen(false)}
      >
        <DialogTitle>Duplicate Skill Detected</DialogTitle>
        <DialogContent>
          <DialogContentText>
            A skill with the name "{duplicatePath?.split('/').pop()}" already exists in the registry. 
            Do you want to overwrite it with the new version?
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setConfirmDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleConfirmApprove} variant="contained" color="warning" autoFocus>
            Confirm Update
          </Button>
        </DialogActions>
      </Dialog>

      <Snackbar 
        open={snackbar.open} 
        autoHideDuration={4000} 
        onClose={handleCloseSnackbar}
      >
        <Alert onClose={handleCloseSnackbar} severity={snackbar.severity} sx={{ width: '100%' }}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Container>
  );
};
