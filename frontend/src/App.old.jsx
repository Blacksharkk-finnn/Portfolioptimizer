import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  CircularProgress,
  Alert,
  Button,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  LinearProgress
} from '@mui/material';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Area, AreaChart } from 'recharts';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import WarningIcon from '@mui/icons-material/Warning';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import AssignmentIcon from '@mui/icons-material/Assignment';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';

const API_BASE = '';

function App() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [symbol, setSymbol] = useState('AAPL');
  const [marketData, setMarketData] = useState([]);
  const [sentiment, setSentiment] = useState(null);
  const [biasScores, setBiasScores] = useState(null);
  const [portfolio, setPortfolio] = useState(null);
  const [optimizationOpen, setOptimizationOpen] = useState(false);
  const [optimizationResult, setOptimizationResult] = useState(null);
  const [optimizationLoading, setOptimizationLoading] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Load market data
      const marketRes = await fetch(`${API_BASE}/api/market-data/${symbol}`);
      const marketJson = await marketRes.json();
      setMarketData(marketJson.data || []);

      // Load sentiment
      const sentimentRes = await fetch(`${API_BASE}/api/sentiment/${symbol}`);
      const sentimentJson = await sentimentRes.json();
      setSentiment(sentimentJson);

      // Mock bias scores for demo
      setBiasScores({
        disposition_effect: 0.65,
        loss_aversion: 0.72,
        overconfidence: 0.48,
        recency_bias: 0.55,
        herding_behavior: 0.38,
        confirmation_bias: 0.42,
        anchoring_bias: 0.61,
        regret_aversion: 0.33
      });

      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  const handleSymbolChange = () => {
    loadData();
  };

  const handleOptimization = async () => {
    try {
      setOptimizationLoading(true);
      setOptimizationOpen(true);
      
      const response = await fetch('/api/optimization/optimize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          portfolio_id: 'demo-portfolio',
          assets: ['AAPL', 'MSFT', 'GOOGL'],
          method: 'behavioral_mvo',
          constraints: null
        })
      });
      
      if (!response.ok) throw new Error('Optimization failed');
      
      const result = await response.json();
      
      // Fallback mock data if response is incomplete
      const mockResult = {
        ...result,
        recommended_weights: result.weights || {
          'AAPL': 0.40,
          'MSFT': 0.35,
          'GOOGL': 0.25
        },
        current_weights: {
          'AAPL': 0.33,
          'MSFT': 0.33,
          'GOOGL': 0.34
        },
        expected_return: result.expected_return || 0.098,
        expected_risk: result.expected_volatility || 0.164,
        sharpe_ratio: result.sharpe_ratio || 0.45,
        rationale: 'Based on your high disposition effect (65%) and loss aversion (72%), the optimization reduces concentration risk and increases diversification to minimize emotional decision-making.'
      };
      
      setOptimizationResult(mockResult);
      setOptimizationLoading(false);
    } catch (err) {
      setError(err.message);
      setOptimizationLoading(false);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom>
          Behavioral Portfolio Optimizer
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          Real-time bias detection and portfolio optimization
        </Typography>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {/* Symbol Selector */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Box display="flex" gap={2} alignItems="center">
          <TextField
            label="Symbol"
            value={symbol}
            onChange={(e) => setSymbol(e.target.value.toUpperCase())}
            size="small"
          />
          <Button variant="contained" onClick={handleSymbolChange}>
            Load Data
          </Button>
        </Box>
      </Paper>

      <Grid container spacing={3}>
        {/* Market Data Chart */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Market Data - {symbol}
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={marketData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="close" stroke="#8884d8" name="Close Price" />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Sentiment Card */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Sentiment Analysis
              </Typography>
              {sentiment && (
                <>
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="body2" color="text.secondary">
                      Sentiment Score
                    </Typography>
                    <Typography variant="h4" color={sentiment.sentiment_score > 0 ? 'success.main' : 'error.main'}>
                      {sentiment.sentiment_score > 0 ? '+' : ''}{sentiment.sentiment_score}
                    </Typography>
                  </Box>
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="body2" color="text.secondary">
                      Confidence
                    </Typography>
                    <Typography variant="h5">
                      {(sentiment.confidence * 100).toFixed(0)}%
                    </Typography>
                  </Box>
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="body2" color="text.secondary">
                      Volume Mentions
                    </Typography>
                    <Typography variant="h5">
                      {sentiment.volume_mentions}
                    </Typography>
                  </Box>
                </>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Bias Scores */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Behavioral Bias Detection
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={biasScores ? Object.entries(biasScores).map(([key, value]) => ({
                name: key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
                score: value * 100
              })) : []}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
                <YAxis />
                <Tooltip />
                <Bar dataKey="score" fill="#82ca9d" name="Bias Score %" />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Portfolio Summary */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Portfolio Summary
              </Typography>
              <Box sx={{ mt: 2 }}>
                <Typography variant="body2" color="text.secondary">
                  Total Value
                </Typography>
                <Typography variant="h4">
                  $125,430.50
                </Typography>
              </Box>
              <Box sx={{ mt: 2 }}>
                <Typography variant="body2" color="text.secondary">
                  Today's Return
                </Typography>
                <Typography variant="h5" color="success.main">
                  +$1,240.30 (+0.99%)
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Optimization Recommendation */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Optimization Recommendation
              </Typography>
              <Alert severity="info" sx={{ mt: 2 }}>
                Your portfolio shows high disposition effect (65%) and loss aversion (72%). 
                Consider rebalancing to reduce emotional trading.
              </Alert>
              <Button variant="contained" sx={{ mt: 2 }} fullWidth onClick={handleOptimization}>
                View Optimization
              </Button>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Optimization Dialog */}
      <Dialog open={optimizationOpen} onClose={() => setOptimizationOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>Portfolio Optimization Results</DialogTitle>
        <DialogContent>
          {optimizationLoading ? (
            <Box display="flex" justifyContent="center" p={4}>
              <CircularProgress />
            </Box>
          ) : optimizationResult ? (
            <>
              <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
                Recommended Allocation
              </Typography>
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Symbol</TableCell>
                      <TableCell align="right">Current Weight</TableCell>
                      <TableCell align="right">Recommended Weight</TableCell>
                      <TableCell align="right">Change</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {optimizationResult.recommended_weights && Object.entries(optimizationResult.recommended_weights).map(([symbol, weight]) => {
                      const currentWeight = optimizationResult.current_weights?.[symbol] || 0;
                      const change = ((weight - currentWeight) * 100).toFixed(2);
                      return (
                        <TableRow key={symbol}>
                          <TableCell>{symbol}</TableCell>
                          <TableCell align="right">{(currentWeight * 100).toFixed(2)}%</TableCell>
                          <TableCell align="right">{(weight * 100).toFixed(2)}%</TableCell>
                          <TableCell align="right" sx={{ color: change > 0 ? 'success.main' : 'error.main' }}>
                            {change > 0 ? '+' : ''}{change}%
                          </TableCell>
                        </TableRow>
                      );
                    })}
                  </TableBody>
                </Table>
              </TableContainer>
              
              <Box sx={{ mt: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Expected Performance
                </Typography>
                <Grid container spacing={2}>
                  <Grid item xs={4}>
                    <Typography variant="body2" color="text.secondary">Expected Return</Typography>
                    <Typography variant="h6">{(optimizationResult.expected_return * 100).toFixed(2)}%</Typography>
                  </Grid>
                  <Grid item xs={4}>
                    <Typography variant="body2" color="text.secondary">Expected Risk</Typography>
                    <Typography variant="h6">{(optimizationResult.expected_risk * 100).toFixed(2)}%</Typography>
                  </Grid>
                  <Grid item xs={4}>
                    <Typography variant="body2" color="text.secondary">Sharpe Ratio</Typography>
                    <Typography variant="h6">{optimizationResult.sharpe_ratio?.toFixed(2) || 'N/A'}</Typography>
                  </Grid>
                </Grid>
              </Box>

              {optimizationResult.rationale && (
                <Alert severity="info" sx={{ mt: 3 }}>
                  {optimizationResult.rationale}
                </Alert>
              )}
            </>
          ) : null}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOptimizationOpen(false)}>Close</Button>
          <Button variant="contained" onClick={() => setOptimizationOpen(false)}>Accept Recommendation</Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}

export default App;
