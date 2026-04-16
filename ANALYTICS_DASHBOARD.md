# REVENUE & ANALYTICS DASHBOARD
# Track your SaaS metrics that matter: MRR, churn, LTV, CAC

## KEY SaaS METRICS TO TRACK

### 1. Monthly Recurring Revenue (MRR)
**Definition:** Total predictable revenue from subscriptions
**Formula:** (Active Customers) × (Average Plan Price)
**Target:** $1,000+ MRR = viable business

Example:
- 10 customers on Starter ($15) = $150
- 15 customers on Professional ($49) = $735
- 2 customers on Enterprise ($199) = $398
- **Total MRR = $1,283**

### 2. Annual Recurring Revenue (ARR)
**Definition:** MRR × 12
**Formula:** MRR × 12
**Target:** $12,000+ ARR = fundable/sellable

From example above: $1,283 × 12 = $15,396 ARR

### 3. Churn Rate
**Definition:** Percentage of customers who cancel each month
**Formula:** (Customers Lost This Month) / (Customers at Start of Month) × 100
**Target:** <5% monthly churn

Example:
- Started month with 50 customers
- 2 canceled
- Churn = 2/50 × 100 = 4%

**What it means:**
- 3% churn: Can sustain indefinitely
- 5% churn: Need 5% month-over-month growth just to stay flat
- 7%+ churn: Unsustainable - need to fix product

### 4. Customer Acquisition Cost (CAC)
**Definition:** Money spent to acquire one customer
**Formula:** (Marketing Spend) / (New Customers)
**Target:** <$100 per customer

Example:
- Spent $500 on email outreach
- Got 8 new customers
- CAC = $500 / 8 = $62.50

### 5. Customer Lifetime Value (LTV)
**Definition:** Total profit from one customer
**Formula:** (Average Customer Monthly Profit) × (Months Active)
**Target:** LTV > 3x CAC

Example with 5% churn:
- Average customer lasts: 1 / 0.05 = 20 months
- Monthly profit per customer: $40 (after payment processing)
- LTV = $40 × 20 = $800
- CAC = $62.50
- LTV/CAC ratio = 12.8x ✅ Excellent!

### 6. Payback Period
**Definition:** Months to recoup customer acquisition cost
**Formula:** CAC / (Average Monthly Profit)
**Target:** <3 months

Example:
- CAC = $62.50
- Monthly profit = $40
- Payback = $62.50 / $40 = 1.56 months

### 7. Magic Number
**Definition:** Indicates growth efficiency
**Formula:** (MRR Growth) / (Prior Month Marketing Spend)
**Target:** >0.75

Example:
- Last month MRR: $1,000
- This month MRR: $1,300
- MRR growth: $300
- Marketing spent last month: $500
- Magic Number = $300 / $500 = 0.6 (need to improve)

---

## TRACKING SPREADSHEET

Create this in Google Sheets and update daily/weekly:

### Daily Metrics
| Date | New Signups | New Customers | Cancellations | Downgrades | Revenue (Day) | Notes |
|------|-------------|--------------|---------------|-----------|---------------|-------|
| 2024-01-15 | 5 | 2 | 0 | 0 | $98 | Cold email campaign |
| 2024-01-16 | 3 | 1 | 0 | 0 | $49 | Normal traffic |
| 2024-01-17 | 8 | 3 | 1 | 0 | $95 | Social media post |

### Monthly Summary
| Month | Starting Customers | New Customers | Cancellations | Ending Customers | MRR | Growth % | Churn % |
|-------|-------------------|---------------|---------------|-----------------|-----|---------|---------|
| Jan | 0 | 15 | 0 | 15 | $585 | ∞ | 0% |
| Feb | 15 | 22 | 1 | 36 | $1,404 | 140% | 6.7% |
| Mar | 36 | 35 | 2 | 69 | $2,681 | 91% | 5.6% |

### Revenue Breakdown by Plan
| Plan | Customers | Monthly Revenue | % of Total |
|-----|-----------|-----------------|-----------|
| Starter ($15) | 25 | $375 | 14% |
| Professional ($49) | 40 | $1,960 | 73% |
| Enterprise ($199) | 3 | $597 | 13% |
| **TOTAL** | **68** | **$2,932** | **100%** |

### Cost Analysis
| Category | Cost | % of Revenue |
|----------|------|-------------|
| Email Marketing (SendGrid) | $50 | 1.7% |
| Hosting (DigitalOcean) | $27 | 0.9% |
| Payment Processing (Stripe 2.9% + $0.30) | $85 | 2.9% |
| Tools & Integrations | $30 | 1.0% |
| Your Time (~5 hours/week) | $400 | 13.6% |
| **TOTAL COSTS** | **$592** | **~20%** |
| **PROFIT** | **$2,340** | **~80%** |

---

## MONTHLY GROWTH PROJECTIONS

Starting with acquisition strategy from EMAIL_SALES_SEQUENCE.md:

### Conservative Scenario (5% new customers/week from cold email)
| Month | Total Customers | MRR | Revenue (Annual Projection) |
|-------|-----------------|-----|---------------------------|
| 1 | 5 | $196 | $2,352 |
| 2 | 15 | $584 | $7,008 |
| 3 | 30 | $1,168 | $14,016 |
| 4 | 50 | $1,950 | $23,400 |
| 5 | 75 | $2,925 | $35,100 |
| 6 | 105 | $4,095 | $49,140 |
| 12 | 300+ | $11,700+ | $140,400+ |

### Aggressive Scenario (10% new customers/week + paid ads)
| Month | Total Customers | MRR | Revenue (Annual Projection) |
|-------|-----------------|-----|---------------------------|
| 1 | 10 | $390 | $4,680 |
| 2 | 30 | $1,170 | $14,040 |
| 3 | 75 | $2,925 | $35,100 |
| 4 | 150 | $5,850 | $70,200 |
| 5 | 275 | $10,725 | $128,700 |
| 6 | 450 | $17,550 | $210,600 |
| 12 | 1,500+ | $58,500+ | $702,000+ |

---

## DASHBOARD Python Code

```python
import json
from datetime import datetime, timedelta
from typing import Dict, List

class SaaSMetrics:
    """Track all your SaaS metrics in one place"""
    
    def __init__(self):
        self.metrics = {}
    
    def calculate_mrr(self, customers: List[Dict]) -> float:
        """Calculate Monthly Recurring Revenue"""
        return sum(c['monthly_price'] for c in customers if c['active'])
    
    def calculate_arr(self, mrr: float) -> float:
        """Calculate Annual Recurring Revenue"""
        return mrr * 12
    
    def calculate_churn(self, 
                       customers_start: int, 
                       customers_canceled: int) -> float:
        """Calculate monthly churn rate"""
        if customers_start == 0:
            return 0
        return (customers_canceled / customers_start) * 100
    
    def calculate_cac(self, 
                     marketing_spend: float,
                     new_customers: int) -> float:
        """Calculate Customer Acquisition Cost"""
        if new_customers == 0:
            return 0
        return marketing_spend / new_customers
    
    def calculate_ltv(self,
                     monthly_profit: float,
                     monthly_churn: float) -> float:
        """Calculate Customer Lifetime Value"""
        if monthly_churn == 0:
            return float('inf')
        months_active = 1 / (monthly_churn / 100)
        return monthly_profit * months_active
    
    def calculate_payback_period(self,
                                cac: float,
                                monthly_profit: float) -> float:
        """Months to recoup customer acquisition cost"""
        if monthly_profit == 0:
            return float('inf')
        return cac / monthly_profit
    
    def generate_report(self, data: Dict) -> Dict:
        """Generate full metrics report"""
        
        mrr = self.calculate_mrr(data['customers'])
        arr = self.calculate_arr(mrr)
        churn = self.calculate_churn(
            data['customers_start_month'],
            data['customers_canceled']
        )
        cac = self.calculate_cac(
            data['marketing_spend'],
            data['new_customers']
        )
        ltv = self.calculate_ltv(
            data['avg_monthly_profit'],
            churn
        )
        payback = self.calculate_payback_period(cac, data['avg_monthly_profit'])
        
        return {
            'timestamp': datetime.now().isoformat(),
            'mrr': round(mrr, 2),
            'arr': round(arr, 2),
            'total_customers': len(data['customers']),
            'active_customers': len([c for c in data['customers'] if c['active']]),
            'churn_rate': round(churn, 2),
            'cac': round(cac, 2),
            'ltv': round(ltv, 2) if ltv != float('inf') else 'High',
            'ltv_to_cac_ratio': round(ltv / cac, 1) if cac > 0 else 'High',
            'payback_months': round(payback, 1) if payback != float('inf') else '<1',
            'health': self.get_health_score(
                churn,
                cac,
                ltv,
                data['avg_monthly_profit']
            )
        }
    
    def get_health_score(self, churn, cac, ltv, profit) -> str:
        """Get overall business health score"""
        
        score = 0
        
        # Churn (lower is better)
        if churn < 3:
            score += 25
        elif churn < 5:
            score += 20
        elif churn < 7:
            score += 10
        
        # CAC payback (lower is better)
        if cac < 50:
            score += 25
        elif cac < 100:
            score += 20
        elif cac < 200:
            score += 10
        
        # LTV/CAC ratio (higher is better)
        if isinstance(ltv, float) and ltv > cac * 5:
            score += 25
        elif isinstance(ltv, float) and ltv > cac * 3:
            score += 20
        elif isinstance(ltv, float) and ltv > cac:
            score += 10
        
        # Profitability
        if profit > 1000:
            score += 25
        elif profit > 500:
            score += 20
        elif profit > 100:
            score += 10
        
        if score >= 90:
            return "🟢 Excellent - High growth potential"
        elif score >= 70:
            return "🟡 Good - On track for success"
        elif score >= 50:
            return "🟠 Fair - Focus on unit economics"
        else:
            return "🔴 Poor - Need to make changes"

# Example usage
if __name__ == "__main__":
    
    metrics = SaaSMetrics()
    
    # Your current data
    data = {
        'customers': [
            {'monthly_price': 15, 'active': True},  # Starter customers
            {'monthly_price': 49, 'active': True},
            {'monthly_price': 49, 'active': True},
            {'monthly_price': 199, 'active': True},  # Enterprise
        ],
        'customers_start_month': 4,
        'customers_canceled': 0,
        'new_customers': 4,
        'marketing_spend': 200,
        'avg_monthly_profit': 200,
    }
    
    report = metrics.generate_report(data)
    
    print("\n" + "="*60)
    print("📊 SAAS METRICS DASHBOARD")
    print("="*60)
    print(f"MRR: ${report['mrr']:,.2f}")
    print(f"ARR: ${report['arr']:,.2f}")
    print(f"Total Customers: {report['total_customers']}")
    print(f"Churn Rate: {report['churn_rate']}%")
    print(f"CAC: ${report['cac']:,.2f}")
    print(f"LTV: ${report['ltv']:,.2f}" if isinstance(report['ltv'], float) else f"LTV: {report['ltv']}")
    print(f"LTV/CAC Ratio: {report['ltv_to_cac_ratio']}x")
    print(f"Payback Period: {report['payback_months']} months")
    print(f"\nHealth: {report['health']}")
    print("="*60 + "\n")
```

---

## WEEKLY ACTION ITEMS

- [ ] Update customer list in spreadsheet
- [ ] Calculate this week's MRR
- [ ] Calculate CAC from marketing spend
- [ ] Check churn (any cancellations?)
- [ ] Review growth rate vs targets
- [ ] Celebrate wins! 🎉
- [ ] Plan next week's marketing

---

## RED FLAGS TO WATCH

🔴 Churn > 7%
→ Your product/service isn't delivering value

🔴 CAC > 200
→ Customer acquisition is too expensive

🔴 LTV/CAC < 1
→ You're losing money on each customer

🔴 MRR flat for 2+ months
→ Growth has stalled, need to change strategy

🔴 Payback > 12 months
→ Too long to recover acquisition costs

---

## GREEN FLAGS TO CELEBRATE

🟢 Churn < 3%
→ Customers love your product!

🟢 CAC < $50
→ Efficient customer acquisition

🟢 LTV/CAC > 3x
→ Healthy, scalable business

🟢 Payback < 3 months
→ Quick return on customer investment

🟢 MRR growing 10%+ month-over-month
→ Strong growth trajectory
