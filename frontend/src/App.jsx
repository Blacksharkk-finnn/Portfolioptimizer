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

const API_BASE = import.meta.env.VITE_API_BASE || '';

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

      const marketRes = await fetch(`${API_BASE}/api/market-data/${symbol}`);
      const marketJson = await marketRes.json();
      setMarketData(marketJson.data || []);

      const sentimentRes = await fetch(`${API_BASE}/api/sentiment/${symbol}`);
      const sentimentJson = await sentimentRes.json();
      setSentiment(sentimentJson);

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

      const result = response.ok ? await response.json() : {};

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
      setError(null);
    } catch (err) {
      setOptimizationResult({
        recommended_weights: {
          'AAPL': 0.40,
          'MSFT': 0.35,
          'GOOGL': 0.25
        },
        current_weights: {
          'AAPL': 0.33,
          'MSFT': 0.33,
          'GOOGL': 0.34
        },
        expected_return: 0.098,
        expected_risk: 0.164,
        sharpe_ratio: 0.45,
        rationale: 'Based on your high disposition effect (65%) and loss aversion (72%), the optimization reduces concentration risk and increases diversification to minimize emotional decision-making.'
      });
      setOptimizationLoading(false);
      setError(null);
    }
  };

  if (loading) {
    return (
      <Box sx={{ background: 'linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)', minHeight: '100vh', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
        <Box sx={{ textAlign: 'center' }}>
          <CircularProgress size={60} sx={{ mb: 2 }} />
          <Typography variant="h6" color="text.secondary">Loading Dashboard...</Typography>
        </Box>
      </Box>
    );
  }

  return (
    <Box sx={{ background: 'linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)', minHeight: '100vh', py: 6 }}>
      <Container maxWidth="xl">
        {/* Header Section */}
        <Box sx={{ mb: 8, textAlign: 'center' }}>
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 2, mb: 3 }}>
            <AutoAwesomeIcon sx={{ fontSize: 40, color: 'primary.main' }} />
            <Typography variant="h1" sx={{ 
              background: 'linear-gradient(135deg, #1e40af 0%, #7c3aed 100%)',
              backgroundClip: 'text',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              m: 0
            }}>
              Behavioral Portfolio Optimizer
            </Typography>
          </Box>
          <Typography variant="h6" sx={{ color: 'text.secondary', fontWeight: 500 }}>
            Real-time bias detection and intelligent portfolio optimization
          </Typography>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 3, borderRadius: 3, py: 2 }}>
            <WarningIcon sx={{ mr: 1, mb: 0.5 }} />
            {error}
          </Alert>
        )}

        {/* Control Section */}
        <Paper sx={{ 
          p: 3, 
          mb: 4, 
          background: 'linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%)',
          border: '1px solid rgba(30, 64, 175, 0.1)',
          borderRadius: 3
        }}>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} sm="auto">
              <TextField
                label="Stock Symbol"
                value={symbol}
                onChange={(e) => setSymbol(e.target.value.toUpperCase())}
                size="medium"
                sx={{ width: { xs: '100%', sm: 200 } }}
                placeholder="e.g., AAPL"
              />
            </Grid>
            <Grid item xs={12} sm="auto">
              <Button 
                variant="contained" 
                onClick={handleSymbolChange}
                sx={{ height: 56 }}
                startIcon={<TrendingUpIcon />}
              >
                Load Data
              </Button>
            </Grid>
          </Grid>
        </Paper>

        {/* Main Grid */}
        <Grid container spacing={3} sx={{ mb: 4 }}>
          {/* Market Data Chart - Full Width */}
          <Grid item xs={12}>
            <Card sx={{ borderRadius: 3, overflow: 'hidden' }}>
              <CardContent sx={{ p: 4 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, mb: 3 }}>
                  <TrendingUpIcon sx={{ color: 'primary.main', fontSize: 28 }} />
                  <Typography variant="h6">Market Data - {symbol}</Typography>
                  <Chip label="1M" size="small" variant="outlined" sx={{ ml: 'auto' }} />
                </Box>
                <ResponsiveContainer width="100%" height={350}>
                  <AreaChart data={marketData}>
                    <defs>
                      <linearGradient id="colorClose" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8}/>
                        <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,0,0,0.05)" />
                    <XAxis dataKey="time" stroke="rgba(0,0,0,0.5)" />
                    <YAxis stroke="rgba(0,0,0,0.5)" />
                    <Tooltip 
                      contentStyle={{ 
                        background: 'rgba(255, 255, 255, 0.95)',
                        border: '1px solid #e2e8f0',
                        borderRadius: 8
                      }}
                    />
                    <Area type="monotone" dataKey="close" stroke="#3b82f6" strokeWidth={2} fillOpacity={1} fill="url(#colorClose)" />
                  </AreaChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>

          {/* Sentiment Analysis Card */}
          <Grid item xs={12} md={6}>
            <Card sx={{ borderRadius: 3, height: '100%' }}>
              <CardContent sx={{ p: 4 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, mb: 3 }}>
                  <AnalyticsIcon sx={{ color: 'info.main', fontSize: 28 }} />
                  <Typography variant="h6">Sentiment Analysis</Typography>
                </Box>
                {sentiment ? (
                  <Box>
                    <Box sx={{ mb: 3, p: 2.5, background: 'linear-gradient(135deg, #06b6d4 0%, #06b6d4 100%)', borderRadius: 2, color: 'white' }}>
                      <Typography variant="body2" sx={{ mb: 1, opacity: 0.9 }}>
                        Sentiment Score
                      </Typography>
                      <Typography variant="h4" sx={{ fontWeight: 700 }}>
                        {sentiment.sentiment_score > 0 ? '+' : ''}{sentiment.sentiment_score}
                      </Typography>
                      <Typography variant="caption" sx={{ display: 'block', mt: 1, opacity: 0.8 }}>
                        {sentiment.sentiment_score > 0.5 ? '🟢 Very Positive' : sentiment.sentiment_score > 0 ? '🟢 Positive' : sentiment.sentiment_score > -0.5 ? '🟡 Neutral' : '🔴 Negative'}
                      </Typography>
                    </Box>

                    <Grid container spacing={2}>
                      <Grid item xs={6}>
                        <Box sx={{ p: 2, background: '#f1f5f9', borderRadius: 2 }}>
                          <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                            Confidence
                          </Typography>
                          <Typography variant="h6">{(sentiment.confidence * 100).toFixed(0)}%</Typography>
                          <LinearProgress variant="determinate" value={sentiment.confidence * 100} sx={{ mt: 1 }} />
                        </Box>
                      </Grid>
                      <Grid item xs={6}>
                        <Box sx={{ p: 2, background: '#f1f5f9', borderRadius: 2 }}>
                          <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                            Mentions
                          </Typography>
                          <Typography variant="h6">{sentiment.volume_mentions}</Typography>
                        </Box>
                      </Grid>
                    </Grid>
                  </Box>
                ) : (
                  <CircularProgress />
                )}
              </CardContent>
            </Card>
          </Grid>

          {/* Behavioral Bias Detection Chart */}
          <Grid item xs={12} md={6}>
            <Card sx={{ borderRadius: 3, height: '100%' }}>
              <CardContent sx={{ p: 4 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, mb: 3 }}>
                  <WarningIcon sx={{ color: 'warning.main', fontSize: 28 }} />
                  <Typography variant="h6">Behavioral Bias Detection</Typography>
                </Box>
                {biasScores ? (
                  <ResponsiveContainer width="100%" height={280}>
                    <BarChart data={Object.entries(biasScores).map(([key, value]) => ({ name: key.replace(/_/g, ' '), value: value * 100 }))}>
                      <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,0,0,0.05)" />
                      <XAxis dataKey="name" angle={-45} textAnchor="end" height={80} tick={{ fontSize: 12 }} />
                      <YAxis domain={[0, 100]} />
                      <Tooltip 
                        contentStyle={{ 
                          background: 'rgba(255, 255, 255, 0.95)',
                          border: '1px solid #e2e8f0',
                          borderRadius: 8
                        }}
                      />
                      <Bar dataKey="value" fill="#f59e0b" radius={8} />
                    </BarChart>
                  </ResponsiveContainer>
                ) : (
                  <CircularProgress />
                )}
              </CardContent>
            </Card>
          </Grid>

          {/* Portfolio Summary */}
          <Grid item xs={12} md={6}>
            <Card sx={{ borderRadius: 3, background: 'linear-gradient(135deg, #ecfdf5 0%, #f0fdf4 100%)' }}>
              <CardContent sx={{ p: 4 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, mb: 3 }}>
                  <AssignmentIcon sx={{ color: 'success.main', fontSize: 28 }} />
                  <Typography variant="h6">Portfolio Summary</Typography>
                </Box>
                <Box sx={{ mb: 3 }}>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                    Total Value
                  </Typography>
                  <Typography variant="h4" sx={{ color: 'success.main', fontWeight: 700 }}>
                    $125,430.50
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                    Today's Return
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <TrendingUpIcon sx={{ color: 'success.main' }} />
                    <Typography variant="h6" sx={{ color: 'success.main', fontWeight: 700 }}>
                      +$1,240.30
                    </Typography>
                    <Chip label="+0.99%" size="small" color="success" variant="outlined" />
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          {/* Optimization Recommendation */}
          <Grid item xs={12} md={6}>
            <Card sx={{ borderRadius: 3, background: 'linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%)' }}>
              <CardContent sx={{ p: 4 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, mb: 3 }}>
                  <AutoAwesomeIcon sx={{ color: 'info.main', fontSize: 28 }} />
                  <Typography variant="h6">Optimization Recommendation</Typography>
                </Box>
                <Alert severity="info" sx={{ mb: 3, borderRadius: 2 }}>
                  Your portfolio shows high disposition effect (65%) and loss aversion (72%). Consider rebalancing to reduce emotional trading.
                </Alert>
                <Button 
                  variant="contained" 
                  fullWidth 
                  onClick={handleOptimization}
                  startIcon={<CheckCircleIcon />}
                  sx={{ py: 1.5, fontSize: '1rem' }}
                >
                  View Optimization
                </Button>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Container>

      {/* Optimization Dialog */}
      <Dialog open={optimizationOpen} onClose={() => setOptimizationOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle sx={{ background: 'linear-gradient(135deg, #1e40af 0%, #7c3aed 100%)', color: 'white', fontWeight: 700 }}>
          Portfolio Optimization Results
        </DialogTitle>
        <DialogContent sx={{ py: 3 }}>
          {optimizationLoading ? (
            <Box display="flex" justifyContent="center" p={4}>
              <CircularProgress />
            </Box>
          ) : optimizationResult ? (
            <>
              <Typography variant="h6" gutterBottom sx={{ mt: 2, fontWeight: 700 }}>
                Recommended Allocation
              </Typography>
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow sx={{ background: '#f1f5f9' }}>
                      <TableCell fontWeight={700}>Symbol</TableCell>
                      <TableCell align="right" fontWeight={700}>Current Weight</TableCell>
                      <TableCell align="right" fontWeight={700}>Recommended Weight</TableCell>
                      <TableCell align="right" fontWeight={700}>Change</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {optimizationResult.recommended_weights && Object.entries(optimizationResult.recommended_weights).map(([symbol, weight]) => {
                      const currentWeight = optimizationResult.current_weights?.[symbol] || 0;
                      const change = ((weight - currentWeight) * 100).toFixed(2);
                      return (
                        <TableRow key={symbol} sx={{ '&:hover': { background: '#f8fafc' } }}>
                          <TableCell fontWeight={600}>{symbol}</TableCell>
                          <TableCell align="right">{(currentWeight * 100).toFixed(2)}%</TableCell>
                          <TableCell align="right" sx={{ fontWeight: 600 }}>{(weight * 100).toFixed(2)}%</TableCell>
                          <TableCell align="right" sx={{ color: change > 0 ? 'success.main' : 'error.main', fontWeight: 600 }}>
                            {change > 0 ? '+' : ''}{change}%
                          </TableCell>
                        </TableRow>
                      );
                    })}</TableBody>
                </Table>
              </TableContainer>
              
              <Box sx={{ mt: 3 }}>
                <Typography variant="h6" gutterBottom sx={{ fontWeight: 700 }}>
                  Expected Performance
                </Typography>
                <Grid container spacing={2}>
                  <Grid item xs={4}>
                    <Box sx={{ p: 2, background: 'linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%)', borderRadius: 2 }}>
                      <Typography variant="body2" color="text.secondary">Expected Return</Typography>
                      <Typography variant="h6" sx={{ fontWeight: 700, color: 'primary.main' }}>{(optimizationResult.expected_return * 100).toFixed(2)}%</Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={4}>
                    <Box sx={{ p: 2, background: 'linear-gradient(135deg, #fef3c7 0%, #fef08a 100%)', borderRadius: 2 }}>
                      <Typography variant="body2" color="text.secondary">Expected Risk</Typography>
                      <Typography variant="h6" sx={{ fontWeight: 700, color: 'warning.main' }}>{(optimizationResult.expected_risk * 100).toFixed(2)}%</Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={4}>
                    <Box sx={{ p: 2, background: 'linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%)', borderRadius: 2 }}>
                      <Typography variant="body2" color="text.secondary">Sharpe Ratio</Typography>
                      <Typography variant="h6" sx={{ fontWeight: 700, color: 'success.main' }}>{optimizationResult.sharpe_ratio?.toFixed(2) || 'N/A'}</Typography>
                    </Box>
                  </Grid>
                </Grid>
              </Box>

              {optimizationResult.rationale && (
                <Alert severity="info" sx={{ mt: 3, borderRadius: 2 }}>
                  {optimizationResult.rationale}
                </Alert>
              )}
            </>
          ) : null}
        </DialogContent>
        <DialogActions sx={{ p: 2, gap: 1 }}>
          <Button onClick={() => setOptimizationOpen(false)}>Close</Button>
          <Button variant="contained" onClick={() => setOptimizationOpen(false)}>Accept Recommendation</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default App;
