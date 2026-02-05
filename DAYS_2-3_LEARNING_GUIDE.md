# DAYS 2-3: BEHAVIORAL FINANCE LEARNING GUIDE

## 📚 Complete Learning Curriculum

This guide covers all essential concepts you need for Days 2-3 to fully understand the Behavioral Portfolio Optimizer project.

---

## DAY 2: BEHAVIORAL FINANCE FUNDAMENTALS

### Learning Objectives
By the end of Day 2, you should understand:
1. Loss aversion and prospect theory
2. Mental accounting and reference points
3. Herding and social proof
4. Anchoring bias and availability heuristics
5. Why traditional MPT fails for real investors

### Module 1: Prospect Theory & Loss Aversion (2 hours)

#### The Kahneman-Tversky Value Function

**Key Insight:** Investors don't evaluate wealth in absolute terms, but relative to a reference point.

**Mathematical Model:**
```
V(x) = {
  x^0.88              if x ≥ 0 (gains)
  -2.25|x|^0.88       if x < 0  (losses)
}
```

Where:
- **0.88 exponent** = Diminishing sensitivity (gains feel less good, losses feel worse)
- **2.25 coefficient** = Loss aversion ratio (losses hurt 2.25x more than gains feel good)

#### Why It Matters
```
Example: Your portfolio goes from $100,000 to $110,000 (gain of $10,000)
Traditional view: Utility increases by fixed amount
Prospect view: You feel good, but not proportionally good

Then it drops to $95,000 (loss of $5,000 from new reference point)
Traditional: Pain is half the original gain
Prospect: Pain is 2.25× stronger than the gain happiness!

Result: You lock in the $10k gain (sell winners) and hold the loss
```

#### Application in Our System
In `portfolio_optimizer.py`:
```python
def apply_prospect_theory(self, returns):
    positive_returns = np.maximum(returns - self.reference_point, 0)
    negative_returns = np.minimum(returns - self.reference_point, 0)
    
    utility = (positive_returns ** 0.88 - 
               self.loss_aversion * ((-negative_returns) ** 0.88))
    return utility
```

**Your Task:**
1. Understand the code in `portfolio_optimizer.py` lines 85-96
2. Draw a graph of the value function (S-shaped curve)
3. Calculate utility for: +$100 gain, -$50 loss, -$100 loss

---

### Module 2: Mental Accounting (1.5 hours)

**Definition:** Investors segment portfolio into separate "mental accounts" with different rules for each.

#### Real-World Example
```
Portfolio: $500,000

Mental Accounts (what investors actually do):
├─ Safety Account (50%): Bonds, Cash = $250,000
│  └─ Rule: "Never lose money"
├─ Growth Account (40%): Stocks = $200,000
│  └─ Rule: "Maximize returns"
└─ Speculation Account (10%): Options, Crypto = $50,000
   └─ Rule: "Have fun with upside"

Problem: Emotionally rational, mathematically suboptimal!
- More bonds than diversification requires
- Separate rules prevent true optimization
- But investor feels secure and engaged
```

#### How We Account For It
In `behavioral_analyzer.py`, we detect:
1. **Holding periods by account** - Losses held longer than gains
2. **Position concentration** - Fewer positions = easier mental accounting
3. **Sector grouping** - Investors group by narrative (tech, healthcare, etc.)

**Your Task:**
1. List your 3 mental accounts for $100K portfolio
2. Assign allocation and rules to each
3. Compare to theoretical optimal (60/40 stocks/bonds)

---

### Module 3: Herding & Social Proof (1 hour)

**Definition:** Following crowd behavior into popular investments.

#### Real Data Example
```
Reddit r/wallstreetbets effect:
- GME before 2021: $17/share, 2% of retail portfolios
- After Reddit hype: $350/share peak, 15-20% of retail portfolios
- Herding component: "Everyone's buying, I should too"
- Regret concern: "I'll miss out if I don't join"

Measurement in our system:
Herfindahl Index = Σ(weight_i)²
- Max = 1.0 (all in one stock)
- Min = 1/n (equal weight across n stocks)
- If Herfindahl >> 1/n = high herding detected
```

#### Algorithm in Our System
```python
def _detect_herding_behavior(self, trades):
    symbol_counts = trades['symbol'].value_counts()
    concentrations = (symbol_counts / len(trades)) ** 2
    herfindahl = concentrations.sum()
    
    # Normalize to 0-1 scale
    score = (herfindahl - min_herfindahl) / (max_herfindahl - min_herfindahl)
    return score
```

**Your Task:**
1. Calculate Herfindahl for: [40%, 30%, 20%, 10%] weights
2. Calculate for: [33%, 33%, 34%] weights
3. Which indicates more herding?

---

### Module 4: Anchoring & Availability (1 hour)

#### Anchoring Bias
**Definition:** Sticking to initial price/target despite new information.

```
Example:
- Buy stock at $50 (anchor price)
- Stock rises to $70 (gain)
- Stock falls to $60 (still up from purchase)
- You feel "breakeven" and hold, waiting for $70

Reality: Stock is at $60 (objectively good)
Anchored mind: Stock must reach $70 anchor to feel good
Result: Missed the opportunity to lock in $10 gain
```

#### How We Detect It
```python
# Trading within narrow ranges = anchoring
first_price = symbol_trades.iloc[0]['price']
subsequent_prices = symbol_trades.iloc[1:]['price']
price_deviations = abs(subsequent_prices - first_price) / first_price

if mean(price_deviations) < 5%:  # Trading in 5% band
    # Anchoring detected
```

#### Availability Heuristic
**Definition:** Overweighting recent/memorable information.

```
Recent news: "Tech stocks are booming!"
→ Investors buy tech disproportionately
→ Available = recently seen = must be important
→ Leads to sector concentration
```

**Your Task:**
1. What's the anchor price for your investments?
2. Are you holding for a specific return target?
3. Would you buy it today at current price?

---

### Module 5: Disposition Effect (1 hour)

**Definition:** Selling winners too early, holding losers too long.

#### The Numbers
Research by Shefrin & Statman:
```
Investors are:
- 1.5-2x more likely to sell winners
- 0.5-0.7x likely to sell losers

Result: Realized gains >> Realized losses
But: Unrealized losses >> Unrealized gains

Effect: Paper losses are very large when they finally sell
```

#### Detection Algorithm
```python
def _detect_disposition_effect(self, trades):
    for sell in sells:
        prior_buy = find_matching_buy(sell)
        return_pct = (sell['price'] - prior_buy['price']) / prior_buy['price']
        
        if return_pct > 0:
            realized_gains += sell_quantity * return_pct
        else:
            realized_losses += abs(sell_quantity * return_pct)
    
    disposition_ratio = realized_gains / (realized_gains + realized_losses)
    # > 0.5 = disposing winners more than losers
```

**Your Task:**
1. Calculate your disposition ratio from trades
2. Compare to 0.5 baseline
3. Why do you hold losers?

---

### Module 6: Recency Bias (45 minutes)

**Definition:** Overweighting recent events in decisions.

```
3-year performance:
Year 1: S&P 500 +30%
Year 2: S&P 500 -10%
Year 3: S&P 500 +25%

Average return: 14.3% annually

Recency bias investor:
"Year 3 was great! I should put more in stocks!"
Ignores: Year 2 pain was very real

Reality: Recent good times make bad times feel less likely
→ Increases risk exposure at market tops
→ Decreases risk exposure at market bottoms
→ OPPOSITE of what you should do
```

#### Our Detection
```python
def _detect_recency_bias(self, trades):
    midpoint = trades['trade_date'].min() + (max - min) / 2
    recent_trades = len(trades[trade_date > midpoint])
    
    recent_ratio = recent_trades / len(trades)
    # If > 0.7, clearly concentrated in recent period
```

**Your Task:**
1. Look at your trading history
2. Is >70% in the last 6 months?
3. Did market conditions change?

---

### Summary: Why Real Investors Aren't Rational

Traditional MPT assumes:
- ❌ Investors maximize expected utility
- ❌ Risk perception = Standard deviation
- ❌ Decisions based on all available info
- ❌ No emotions involved

Real investors:
- ✅ Mental accounting (separate buckets)
- ✅ Loss aversion (asymmetric pain)
- ✅ Anchoring (stuck on past prices)
- ✅ Herding (follow the crowd)
- ✅ Recency (recent = relevant)
- ✅ Regret aversion (avoid past mistakes)

**Our job:** Build systems that account for this reality.

---

## DAY 3: PORTFOLIO OPTIMIZATION & ML CONCEPTS

### Learning Objectives
By the end of Day 3, you should understand:
1. Modern Portfolio Theory (MPT) and efficient frontier
2. Black-Litterman model and views
3. Risk measures (Sharpe, Sortino, max drawdown)
4. Machine Learning basics for trading
5. How to set up local development environment

---

### Module 1: Modern Portfolio Theory (1.5 hours)

#### The Markowitz Framework
```
Given:
- n assets with returns r₁, r₂, ..., rₙ
- Covariance matrix Σ showing how returns move together

Problem: Find weights w₁, w₂, ..., wₙ that maximize:
  U = E(R) - λ × σ²

Where:
- E(R) = w^T × μ (expected return)
- σ² = w^T × Σ × w (portfolio variance)
- λ = risk aversion parameter (investor-specific)
```

#### Efficient Frontier
```
Return
   |     * (optimal for risk aversion λ₂)
   |    /
   |   /
   |  * (optimal for λ₁)
   | /
   |/_________________ Risk (Volatility)
   
- Left edge: minimum variance portfolio
- Right edge: max return portfolio
- Curve between: all optimal allocations
- Below curve: suboptimal (same return, more risk)
```

#### Constraints in Reality
```
Mathematical optimization wants:
- 50% in best-performing asset
- Zero in worst-performing asset

Real investors need:
- Max position: 30% (avoid overconcentration)
- Min positions: 5 (minimum diversification)
- Min weights: 1% (don't hold tiny positions)
- Sector limits: max 40% in any sector

Our implementation in portfolio_optimizer.py
```

**Your Task:**
1. Create expected returns: [5%, 8%, 12%] for 3 assets
2. Create covariance matrix showing correlations
3. Calculate portfolio return for [40%, 40%, 20%] weights
4. Calculate portfolio volatility

---

### Module 2: Risk Measures (1.5 hours)

#### Sharpe Ratio
```
Definition: Return per unit of risk taken
           
         Portfolio Return - Risk-Free Rate
Sharpe = ─────────────────────────────────
                Portfolio Volatility

Example:
- Portfolio Return: 10%
- Risk-Free Rate: 2%
- Volatility: 15%

Sharpe = (10% - 2%) / 15% = 0.53

Interpretation:
- >1.0: Excellent (good return for risk)
- 0.5-1.0: Good
- <0.5: Marginal
```

#### Sortino Ratio (Better for downside)
```
Difference: Only penalizes downside volatility

         Portfolio Return - Risk-Free Rate
Sortino = ──────────────────────────────────
          Downside Volatility (only negative returns)

Why better?
- Sharpe: "Volatility is bad" (wrong! upside is good)
- Sortino: "Downside is bad" (right!)
- If stock only goes up, Sharpe penalizes it
- Sortino rewards it
```

#### Maximum Drawdown
```
Definition: Largest peak-to-trough decline

Portfolio value over time:
$100,000 ──────────
         │ ↗ $110,000 (peak)
         ↓
$90,000  ├──
         │    ↑ $105,000 (recovery)
         
Max Drawdown = ($100,000 - $90,000) / $100,000 = -10%

Why investors care:
- Tells you worst case psychological pain
- Sharpe ignores this (only sees average)
- Drawdown >30-40% often triggers panic selling
```

#### Calmar Ratio
```
Definition: Annual return / Max Drawdown
           
         Annual Return
Calmar = ──────────────
         Max Drawdown

Example:
- 12% annual return
- 30% max drawdown
- Calmar = 0.4

Higher = better risk-adjusted returns
```

**Your Task:**
1. Calculate Sharpe ratio for: 8% return, 2% risk-free, 12% volatility
2. Calculate Sortino for same, assuming 8% downside volatility
3. Which is higher and why?

---

### Module 3: Black-Litterman Model (1.5 hours)

#### The Problem with MPT
```
Traditional approach:
1. Calculate historical returns
2. Calculate historical covariance
3. Run optimizer with these inputs
4. Get weights that are 90% in whatever had best past returns

Problem: Past returns ≠ Future returns!
Result: Optimizer tends to overconcentrate in whatever
        did well recently (recency bias in code!)
```

#### Black-Litterman Solution
```
Approach:
1. Start with "market equilibrium" weights (what everyone holds)
2. Layer in your personal views: "I think Tech will outperform"
3. Combine with confidence levels
4. Run optimizer on blended returns
5. Get more balanced, less extreme allocations

Formula:
μ_combined = μ_market + τ × P^T × (Ω + P × Σ × P^T)^(-1) × (Q - P × μ_market)

Where:
- τ = uncertainty in views (0.1-0.3)
- P = picking matrix (which assets have views)
- Q = your view returns
- Ω = uncertainty in views (variance)
```

#### Our Implementation
In `portfolio_optimizer.py`:
```python
def _black_litterman_optimization(self, market_returns, cov_matrix):
    # Confidence = 0.5 / (1 + overconfidence)
    confidence = 0.5 / (1 + self.overconfidence)
    tau = confidence
    
    # Combine market returns with your views
    blended_returns = (market_returns + 
                       tau * (your_views - market_returns))
    
    # Optimize on blended returns
    weights = optimize(blended_returns, cov_matrix)
    return weights
```

**Your Task:**
1. List 3 views on future returns
2. Assign confidence to each (1-10 scale)
3. How would this change your allocation?

---

### Module 4: Machine Learning Fundamentals (1.5 hours)

#### Types of Learning
```
1. Supervised Learning
   Input: Trading history + behavioral labels
   Output: Model learns to classify biases
   Example: "This trader is panic selling"

2. Unsupervised Learning
   Input: Trading patterns
   Output: Model groups similar traders
   Example: "This trader resembles 'loss avoider' cluster"

3. Reinforcement Learning
   Input: Market data, portfolio state, possible actions
   Output: Agent learns optimal portfolio decisions
   Example: "Buy Apple when PE<15 and sentiment positive"
```

#### LSTM Networks (For Bias Prediction)
```
Why LSTM?
- Traditional neural networks: inputs independent
- LSTM: remembers previous events
- Sequence matters in trading (e.g., panic follows losses)

Architecture:
Input (30 days of trading) 
  ↓
LSTM Layer 1: 128 units (learn patterns)
  ↓ Dropout (20% regularization)
LSTM Layer 2: 64 units (refine patterns)
  ↓ Dropout
LSTM Layer 3: 32 units (final processing)
  ↓
Dense Layer: 64 units (decision making)
  ↓
Output: 8 bias probabilities

Training:
- Input: Trading sequences + labels (panic, fomo, etc.)
- Loss: Cross-entropy (how wrong are predictions)
- Optimization: Adam (smart gradient descent)
```

#### Reinforcement Learning (Portfolio Management)
```
Environment: Market with price changes
Agent: Portfolio manager
State: Holdings, returns, bias scores, market conditions
Action: Buy/sell decisions
Reward: Risk-adjusted return - behavioral penalties

Example:
State: [40% stocks, 30% bonds, VIX=25, trader_bias=0.8]
Action: Increase stocks to 50%
Outcome: Market rises 2%, trader feels good
Reward: +2% return - 0.1 behavioral penalty = +1.9%

Training: Millions of simulations to learn optimal policy
```

**Your Task:**
1. Draw LSTM network architecture
2. List 5 features for bias prediction
3. What would be good/bad reward signals?

---

### Module 5: Setting Up Local Development (1 hour)

#### System Requirements
```
Minimum:
- Python 3.10+
- 8GB RAM
- 10GB disk space
- Docker & Docker Compose

Recommended:
- Python 3.11
- 16GB RAM
- SSD (faster database)
- 20GB disk space
```

#### Environment Configuration
```
Key files:
- .env.example → .env (your local settings)
- docker-compose.yml (defines all services)
- requirements.txt (Python packages)
- package.json (JavaScript packages)

Environment variables to set:
DATABASE_URL=postgresql://user:pass@localhost/db
REDIS_HOST=localhost
SECRET_KEY=your-secret-key-here
```

#### Docker Services
```
Services that will run:

1. PostgreSQL (database)
   Port: 5432
   Username: zetheta_user
   
2. Redis (cache)
   Port: 6379
   
3. FastAPI (backend)
   Port: 8000
   API docs: http://localhost:8000/docs
   
4. React (frontend)
   Port: 3000
   
5. Prometheus (monitoring)
   Port: 9090
   
6. Grafana (dashboards)
   Port: 3001
```

#### Health Checks
```bash
# Test database
curl http://localhost:5432  # Should refuse (not HTTP)

# Test API
curl http://localhost:8000/health
# Expected: {"status": "healthy", ...}

# Test frontend
curl http://localhost:3000  # Should return HTML

# Test Prometheus
curl http://localhost:9090/api/v1/status/config
# Should return JSON config
```

**Your Task:**
1. Document your system specs
2. List 3 ports that will be used
3. Plan your directory structure

---

## DAYS 2-3 PRACTICAL EXERCISES

### Exercise 1: Calculate Sharpe Ratio
```python
# Given:
portfolio_return = 0.12  # 12%
risk_free_rate = 0.02   # 2%
volatility = 0.18       # 18%

# Calculate:
sharpe = (portfolio_return - risk_free_rate) / volatility
# Your answer:
```

### Exercise 2: Detect Disposition Effect
```
Trades:
1. Buy Apple at $100, Sell at $120 (gain: $20)
2. Buy Microsoft at $200, Sell at $180 (loss: -$20)
3. Buy Tesla at $300, Sell at $330 (gain: $30)
4. Buy Google at $400, Still holding at $350 (loss: -$50 unrealized)

Questions:
1. Realized gain ratio = ?
2. Disposition effect present? (Compare gains vs losses sold)
3. What does unrealized loss suggest?
```

### Exercise 3: Portfolio Optimization
```
Three assets:
           Return  Volatility  Correlation
Apple       8%      15%        
Microsoft   10%     18%        0.6 (with Apple)
Tesla       15%     30%        0.4 (with Apple), 0.7 (with Microsoft)

Questions:
1. What's your expected return for [40%, 40%, 20%]?
2. Calculate portfolio variance
3. If risk-free rate is 2%, what's Sharpe ratio?
```

### Exercise 4: Identify Your Biases
```
Reflect on your own investing:

1. Loss Aversion
   Q: Do you hold losers longer than winners?
   
2. Anchoring
   Q: Do you have a target price you're waiting for?
   
3. Herding
   Q: Do you follow what others are buying?
   
4. Recency
   Q: Are >70% of your trades in last 3 months?
   
5. Overconfidence
   Q: Do you trade more than market benchmark?
```

---

## DAY 3 SETUP CHECKLIST

### Understanding Achieved ✓
- [ ] Prospect theory and loss aversion
- [ ] Mental accounting concept
- [ ] Herding and anchoring biases
- [ ] Modern Portfolio Theory
- [ ] Risk measures (Sharpe, Sortino, Drawdown)
- [ ] Black-Litterman model
- [ ] LSTM networks
- [ ] Reinforcement learning
- [ ] ML concepts for trading

### Preparation Complete ✓
- [ ] System requirements documented
- [ ] Environment variables understood
- [ ] Docker services explained
- [ ] Health check procedures known
- [ ] Port allocations confirmed
- [ ] File structure planned

### Ready for Development ✓
- [ ] Private GitHub repo created (PRIVATE visibility!)
- [ ] .env file configured (from .env.example)
- [ ] Docker Compose tested locally
- [ ] API responds to health check
- [ ] Database connected
- [ ] All ports accessible
- [ ] First commit made

---

## KEY TAKEAWAYS

**Behavioral Finance:**
- Real investors are NOT rational
- Loss aversion = 2.25:1 ratio (losses hurt more)
- Mental accounting = emotional portfolio segments
- Biases cluster: if one bias present, others likely too

**Portfolio Optimization:**
- Efficient frontier = all possible good allocations
- Sharpe ratio = return per risk unit
- Max drawdown = psychological pain threshold
- Black-Litterman = market views + your views

**Machine Learning:**
- LSTM = remembers sequences (good for patterns)
- RL = learns optimal decisions through millions of trials
- Feature engineering = turning raw data into signals
- Training = finding patterns in historical data

**Implementation:**
- Our system detects 8 biases
- Adjusts optimization based on detected biases
- Provides nudges when biases detected
- Backtests before recommending

---

## NEXT STEPS (Day 3)

1. Create private GitHub repository
   - Name: `zetheta-behavioral-portfolio-[yourname]`
   - Visibility: **PRIVATE** (CRITICAL!)
   - Add README with confidentiality notice
   - Enable branch protection rules

2. Configure local environment
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   docker-compose up -d
   curl http://localhost:8000/health
   ```

3. Initialize Git
   ```bash
   git init
   git add .
   git commit -m "Initial project setup - Day 1 completion"
   git branch -M main
   git remote add origin https://github.com/your-username/zetheta-behavioral-portfolio.git
   git push -u origin main
   ```

4. Verify everything works
   - [ ] Docker services running
   - [ ] API responds
   - [ ] Database connected
   - [ ] Ports accessible
   - [ ] Git repository synced

---

**YOU'RE READY FOR DAYS 4-15! 🚀**

*CONFIDENTIAL - Property of Zetheta Algorithms Private Limited*
