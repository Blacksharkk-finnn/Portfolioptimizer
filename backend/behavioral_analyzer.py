"""
Behavioral Finance Analysis Engine
Detects and measures investor biases from trading patterns
"""
from typing import Dict, List, Tuple, Optional
import numpy as np
import pandas as pd
from datetime import datetime, timedelta


class BehavioralEvent:
    """Represents a detected behavioral event"""
    def __init__(self, event_type: str, severity: float, context: Dict):
        self.event_type = event_type
        self.severity = severity
        self.context = context
        self.timestamp = datetime.utcnow()


class BiasScore:
    """Represents bias intensity scores"""
    def __init__(self):
        self.confirmation_bias = 0.0
        self.recency_bias = 0.0
        self.anchoring_bias = 0.0
        self.herding_behavior = 0.0
        self.loss_aversion = 0.0
        self.overconfidence = 0.0
        self.disposition_effect = 0.0
        self.regret_aversion = 0.0
        self.overall_score = 0.0


class BehavioralAnalyzer:
    """
    Core behavioral analysis engine
    Detects investor biases from trading patterns
    """

    def __init__(self):
        self.min_trades = 10  # Minimum trades to make assessment
        self.confidence_threshold = 0.6

    def analyze_user_trades(self, trades: List[Dict]) -> Tuple[BiasScore, List[BehavioralEvent]]:
        """
        Main analysis function
        Returns bias scores and detected behavioral events
        """
        if len(trades) < self.min_trades:
            return BiasScore(), []

        # Convert to DataFrame for easier analysis
        df_trades = pd.DataFrame(trades)
        df_trades['trade_date'] = pd.to_datetime(df_trades['trade_date'])
        df_trades = df_trades.sort_values('trade_date')

        # Calculate various behavioral metrics
        bias_score = BiasScore()
        events = []

        # 1. Disposition Effect (selling winners too early, holding losers too long)
        disposition_effect, disposition_events = self._detect_disposition_effect(df_trades)
        bias_score.disposition_effect = disposition_effect
        events.extend(disposition_events)

        # 2. Loss Aversion (reluctance to sell losers)
        loss_aversion, loss_events = self._detect_loss_aversion(df_trades)
        bias_score.loss_aversion = loss_aversion
        events.extend(loss_events)

        # 3. Overconfidence (excessive trading)
        overconfidence, overconf_events = self._detect_overconfidence(df_trades)
        bias_score.overconfidence = overconfidence
        events.extend(overconf_events)

        # 4. Recency Bias (overweighting recent events)
        recency, recency_events = self._detect_recency_bias(df_trades)
        bias_score.recency_bias = recency
        events.extend(recency_events)

        # 5. Herding Behavior (following crowd)
        herding, herding_events = self._detect_herding_behavior(df_trades)
        bias_score.herding_behavior = herding
        events.extend(herding_events)

        # 6. Confirmation Bias (seeking confirming information)
        confirmation, confirmation_events = self._detect_confirmation_bias(df_trades)
        bias_score.confirmation_bias = confirmation
        events.extend(confirmation_events)

        # 7. Anchoring Bias (holding prices/expectations)
        anchoring, anchoring_events = self._detect_anchoring_bias(df_trades)
        bias_score.anchoring_bias = anchoring
        events.extend(anchoring_events)

        # 8. Regret Aversion (avoiding past mistakes)
        regret, regret_events = self._detect_regret_aversion(df_trades)
        bias_score.regret_aversion = regret
        events.extend(regret_events)

        # Calculate overall bias score
        bias_score.overall_score = (
            disposition_effect + loss_aversion + overconfidence +
            recency + herding + confirmation + anchoring + regret
        ) / 8

        return bias_score, events

    def _detect_disposition_effect(self, trades: pd.DataFrame) -> Tuple[float, List[BehavioralEvent]]:
        """
        Disposition Effect: Tendency to sell winners too early and hold losers too long
        Metric: Ratio of realized gains to realized losses
        """
        events = []

        # Calculate returns on closed positions
        sells = trades[trades['action'] == 'SELL']
        buys = trades[trades['action'] == 'BUY']

        if len(sells) == 0:
            return 0.0, events

        realized_gains = 0
        realized_losses = 0
        sold_positions = 0

        for _, sell in sells.iterrows():
            # Find corresponding buy
            prior_buys = buys[
                (buys['symbol'] == sell['symbol']) &
                (buys['trade_date'] < sell['trade_date'])
            ]

            if len(prior_buys) > 0:
                avg_cost = prior_buys['price'].mean()
                return_pct = (sell['price'] - avg_cost) / avg_cost

                if return_pct > 0:
                    realized_gains += sell['quantity'] * return_pct
                else:
                    realized_losses += abs(sell['quantity'] * return_pct)

                sold_positions += 1

        # Calculate disposition effect score
        if realized_gains + realized_losses > 0:
            disposition_ratio = realized_gains / (realized_gains + realized_losses)
            # Higher ratio = stronger disposition effect (more willing to sell gains)
            score = max(0, disposition_ratio - 0.5) * 2  # 0-1 scale

            if score > 0.7:
                events.append(BehavioralEvent(
                    event_type='disposition_effect',
                    severity=score,
                    context={
                        'realized_gains': realized_gains,
                        'realized_losses': realized_losses,
                        'ratio': disposition_ratio
                    }
                ))

            return score, events

        return 0.0, events

    def _detect_loss_aversion(self, trades: pd.DataFrame) -> Tuple[float, List[BehavioralEvent]]:
        """
        Loss Aversion: Reluctance to realize losses
        Metric: Average holding period for losses vs gains
        """
        events = []

        # Group by symbol and calculate holding periods
        buys = trades[trades['action'] == 'BUY']
        sells = trades[trades['action'] == 'SELL']

        loss_holding_periods = []
        gain_holding_periods = []

        for _, buy in buys.iterrows():
            # Find corresponding sell
            future_sells = sells[
                (sells['symbol'] == buy['symbol']) &
                (sells['trade_date'] > buy['trade_date'])
            ]

            if len(future_sells) > 0:
                sell = future_sells.iloc[0]
                holding_period = (sell['trade_date'] - buy['trade_date']).days

                if sell['price'] < buy['price']:
                    loss_holding_periods.append(holding_period)
                else:
                    gain_holding_periods.append(holding_period)

        # Calculate loss aversion score
        if loss_holding_periods and gain_holding_periods:
            avg_loss_holding = np.mean(loss_holding_periods)
            avg_gain_holding = np.mean(gain_holding_periods)

            # If holding losses longer than gains, indicates loss aversion
            score = min(1.0, avg_loss_holding / (avg_gain_holding + 1))

            if score > 0.6:
                events.append(BehavioralEvent(
                    event_type='loss_aversion',
                    severity=score,
                    context={
                        'avg_loss_holding_days': avg_loss_holding,
                        'avg_gain_holding_days': avg_gain_holding
                    }
                ))

            return score, events

        return 0.0, events

    def _detect_overconfidence(self, trades: pd.DataFrame) -> Tuple[float, List[BehavioralEvent]]:
        """
        Overconfidence: Trading too frequently, excessive turnover
        Metric: Trading frequency relative to market volatility
        """
        events = []

        # Calculate trading frequency
        days_in_period = (trades['trade_date'].max() - trades['trade_date'].min()).days + 1
        num_trades = len(trades)

        if days_in_period < 1:
            return 0.0, events

        trades_per_day = num_trades / days_in_period

        # Benchmark: reasonable investor trades ~1-2 times per month
        benchmark_trades_per_day = 1.5 / 30  # ~0.05 trades per day

        # Calculate overtrading score
        score = min(1.0, trades_per_day / benchmark_trades_per_day)

        if score > 0.7:
            events.append(BehavioralEvent(
                event_type='overconfidence',
                severity=score,
                context={
                    'trades_per_day': trades_per_day,
                    'total_trades': num_trades,
                    'period_days': days_in_period
                }
            ))

        return score, events

    def _detect_recency_bias(self, trades: pd.DataFrame) -> Tuple[float, List[BehavioralEvent]]:
        """
        Recency Bias: Overweighting recent events in decision making
        Metric: Concentration of trades in recent period vs older period
        """
        events = []

        midpoint = trades['trade_date'].min() + (trades['trade_date'].max() - trades['trade_date'].min()) / 2

        recent_trades = trades[trades['trade_date'] > midpoint]
        old_trades = trades[trades['trade_date'] <= midpoint]

        if len(old_trades) == 0:
            return 0.0, events

        recent_ratio = len(recent_trades) / len(trades)

        # If >70% of trades in recent period, indicates recency bias
        score = min(1.0, (recent_ratio - 0.5) * 2)

        if score > 0.6:
            events.append(BehavioralEvent(
                event_type='recency_bias',
                severity=score,
                context={
                    'recent_trade_ratio': recent_ratio,
                    'recent_trades': len(recent_trades),
                    'old_trades': len(old_trades)
                }
            ))

        return score, events

    def _detect_herding_behavior(self, trades: pd.DataFrame) -> Tuple[float, List[BehavioralEvent]]:
        """
        Herding Behavior: Following crowd, buying popular stocks
        Metric: Concentration in most traded symbols
        """
        events = []

        # Get top traded symbols
        symbol_counts = trades['symbol'].value_counts()

        if len(symbol_counts) < 2:
            return 0.0, events

        # Herfindahl index for concentration
        total_trades = len(trades)
        concentrations = (symbol_counts / total_trades) ** 2
        herfindahl = concentrations.sum()

        # Normalize: 0 = diversified, 1 = fully concentrated
        max_possible_herfindahl = 1.0
        min_possible_herfindahl = 1.0 / len(symbol_counts)
        normalized_herfindahl = (herfindahl - min_possible_herfindahl) / (max_possible_herfindahl - min_possible_herfindahl)

        score = min(1.0, normalized_herfindahl)

        if score > 0.6:
            events.append(BehavioralEvent(
                event_type='herding_behavior',
                severity=score,
                context={
                    'top_symbol': symbol_counts.index[0],
                    'top_symbol_concentration': symbol_counts.iloc[0] / total_trades,
                    'unique_symbols': len(symbol_counts)
                }
            ))

        return score, events

    def _detect_confirmation_bias(self, trades: pd.DataFrame) -> Tuple[float, List[BehavioralEvent]]:
        """
        Confirmation Bias: Seeking information that confirms existing beliefs
        Metric: Repeated buying of same stocks without selling
        """
        events = []

        # Count buy operations
        buys = trades[trades['action'] == 'BUY']
        symbol_buy_counts = buys['symbol'].value_counts()

        if len(symbol_buy_counts) == 0:
            return 0.0, events

        # Average buys per symbol
        avg_buys = symbol_buy_counts.mean()
        symbols_repeatedly_bought = (symbol_buy_counts > avg_buys * 1.5).sum()

        if len(symbol_buy_counts) > 0:
            ratio = symbols_repeatedly_bought / len(symbol_buy_counts)
            score = min(1.0, ratio * 2)

            if score > 0.5:
                events.append(BehavioralEvent(
                    event_type='confirmation_bias',
                    severity=score,
                    context={
                        'repeatedly_bought_symbols': symbols_repeatedly_bought,
                        'avg_buys_per_symbol': avg_buys,
                        'max_buys_single_symbol': symbol_buy_counts.max()
                    }
                ))

            return score, events

        return 0.0, events

    def _detect_anchoring_bias(self, trades: pd.DataFrame) -> Tuple[float, List[BehavioralEvent]]:
        """
        Anchoring Bias: Sticking to initial price targets/expectations
        Metric: Distance from initial entry price for same symbols
        """
        events = []

        symbols = trades['symbol'].unique()

        price_deviations = []
        for symbol in symbols:
            symbol_trades = trades[trades['symbol'] == symbol].sort_values('trade_date')

            if len(symbol_trades) > 1:
                first_price = symbol_trades.iloc[0]['price']

                for _, trade in symbol_trades.iloc[1:].iterrows():
                    deviation = abs(trade['price'] - first_price) / first_price
                    price_deviations.append(deviation)

        if price_deviations:
            avg_deviation = np.mean(price_deviations)
            # If trading within small range of initial price, indicates anchoring
            score = min(1.0, 1.0 - avg_deviation)  # Inverted: less deviation = more anchoring

            if score > 0.7:
                events.append(BehavioralEvent(
                    event_type='anchoring_bias',
                    severity=score,
                    context={
                        'avg_price_deviation': avg_deviation,
                        'symbols_analyzed': len(symbols)
                    }
                ))

            return score, events

        return 0.0, events

    def _detect_regret_aversion(self, trades: pd.DataFrame) -> Tuple[float, List[BehavioralEvent]]:
        """
        Regret Aversion: Avoiding/repeating past mistakes
        Metric: Behavioral change after significant losses
        """
        events = []

        # Find significant losses
        trades_with_returns = trades.copy()
        sells = trades[trades['action'] == 'SELL']

        if len(sells) < 5:
            return 0.0, events

        # Calculate returns on closed positions
        significant_losses = []
        for _, sell in sells.iterrows():
            buys = trades[
                (trades['action'] == 'BUY') &
                (trades['symbol'] == sell['symbol']) &
                (trades['trade_date'] < sell['trade_date'])
            ]

            if len(buys) > 0:
                avg_cost = buys['price'].mean()
                loss_pct = (sell['price'] - avg_cost) / avg_cost

                if loss_pct < -0.1:  # 10%+ loss
                    significant_losses.append((sell['trade_date'], loss_pct))

        if len(significant_losses) == 0:
            return 0.0, events

        # Check if behavior changed after losses
        score = min(1.0, len(significant_losses) / len(sells))

        if score > 0.2:
            events.append(BehavioralEvent(
                event_type='regret_aversion',
                severity=score,
                context={
                    'significant_losses': len(significant_losses),
                    'avg_loss_magnitude': np.mean([loss for _, loss in significant_losses]),
                    'total_sells': len(sells)
                }
            ))

        return score, events


def detect_real_time_bias(current_trade: Dict, user_profile: Dict, market_conditions: Dict) -> Optional[BehavioralEvent]:
    """
    Detect behavioral bias at the moment of trade execution
    Returns event if bias detected, None otherwise
    """

    # Panic Selling Detection
    if current_trade['action'] == 'SELL':
        if market_conditions.get('market_down_percent', 0) > 5:  # Market down >5%
            if current_trade.get('last_price_change', 0) < -5:  # Stock down >5%
                return BehavioralEvent(
                    event_type='panic_selling',
                    severity=min(1.0, abs(market_conditions['market_down_percent']) / 20),
                    context={
                        'market_down': market_conditions['market_down_percent'],
                        'stock_down': current_trade['last_price_change'],
                        'trading_volume': market_conditions.get('trading_volume', 0)
                    }
                )

    # FOMO Buying Detection
    if current_trade['action'] == 'BUY':
        if market_conditions.get('market_up_percent', 0) > 5:  # Market up >5%
            if current_trade.get('last_price_change', 0) > 5:  # Stock up >5%
                return BehavioralEvent(
                    event_type='fomo_buying',
                    severity=min(1.0, market_conditions['market_up_percent'] / 20),
                    context={
                        'market_up': market_conditions['market_up_percent'],
                        'stock_up': current_trade['last_price_change'],
                        'news_sentiment': market_conditions.get('sentiment_score', 0)
                    }
                )

    return None
