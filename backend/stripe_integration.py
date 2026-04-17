#!/usr/bin/env python3
"""
STRIPE PAYMENT INTEGRATION
Complete payment processing for SEO Analyzer Pro
Run this to integrate Stripe payments into your backend
"""

import os
import json
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

# Install: pip install stripe

import stripe

# Initialize Stripe
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "sk_test_your_key_here")

router = APIRouter(prefix="/payments", tags=["payments"])

# ============================================================================
# DATA MODELS
# ============================================================================

class CreateCheckoutSession(BaseModel):
    """Request to create a Stripe checkout session"""
    plan: str  # starter, professional, enterprise
    email: str
    name: str
    company: str = None

class CreateCustomer(BaseModel):
    """Create a new Stripe customer"""
    email: str
    name: str
    company: str = None

class CancelSubscription(BaseModel):
    """Cancel a customer's subscription"""
    customer_id: str
    reason: str = None

# ============================================================================
# PRICING CONFIGURATION
# ============================================================================

PRICING = {
    "starter": {
        "name": "Starter",
        "price_monthly": 1500,  # $15.00 in cents
        "price_annual": 15000,   # $150.00 in cents (10% discount)
        "description": "500 keywords/month",
        "features": [
            "500 keywords/month",
            "Basic competitor analysis",
            "Email support",
            "JSON exports"
        ]
    },
    "professional": {
        "name": "Professional",
        "price_monthly": 4900,  # $49.00 in cents
        "price_annual": 49000,   # $490.00 in cents
        "description": "5,000 keywords/month + AI content",
        "features": [
            "5,000 keywords/month",
            "Advanced competitor analysis",
            "AI content generation",
            "Priority support",
            "API access",
            "Zapier integrations"
        ]
    },
    "enterprise": {
        "name": "Enterprise",
        "price_monthly": 19900,  # $199.00 in cents
        "price_annual": 199000,   # $1,990.00 in cents
        "description": "Unlimited + white-label",
        "features": [
            "Unlimited keywords",
            "Custom integrations",
            "Dedicated support",
            "Advanced reporting",
            "White-label option",
            "SLA guarantee"
        ]
    }
}

# ============================================================================
# STRIPE ENDPOINTS
# ============================================================================

@router.post("/create-checkout-session")
async def create_checkout_session(request: CreateCheckoutSession):
    """
    Create a Stripe checkout session
    Returns a URL to redirect user to payment
    """
    
    try:
        plan_config = PRICING.get(request.plan)
        if not plan_config:
            raise HTTPException(status_code=400, detail="Invalid plan")
        
        # Create Stripe checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": f"SEO Analyzer Pro - {plan_config['name']} Plan",
                            "description": plan_config["description"],
                            "metadata": {
                                "plan": request.plan,
                                "company": request.company or "N/A"
                            }
                        },
                        "unit_amount": plan_config["price_monthly"],
                        "recurring": {
                            "interval": "month",
                            "interval_count": 1
                        }
                    },
                    "quantity": 1,
                }
            ],
            customer_email=request.email,
            metadata={
                "customer_name": request.name,
                "plan": request.plan,
                "company": request.company or "N/A"
            },
            mode="subscription",
            success_url="http://localhost:3000/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="http://localhost:3000/canceled",
        )
        
        return {
            "checkout_url": session.url,
            "session_id": session.id,
            "status": "success"
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/create-customer")
async def create_customer(request: CreateCustomer):
    """Create a new Stripe customer"""
    
    try:
        customer = stripe.Customer.create(
            email=request.email,
            name=request.name,
            metadata={"company": request.company or "N/A"}
        )
        
        return {
            "customer_id": customer.id,
            "email": customer.email,
            "status": "success"
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/customer/{customer_id}")
async def get_customer(customer_id: str):
    """Get customer details from Stripe"""
    
    try:
        customer = stripe.Customer.retrieve(customer_id)
        
        # Get their active subscriptions
        subscriptions = stripe.Subscription.list(customer=customer_id)
        
        return {
            "customer_id": customer.id,
            "email": customer.email,
            "name": customer.name,
            "subscriptions": subscriptions.data,
            "status": "success"
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/cancel-subscription")
async def cancel_subscription(request: CancelSubscription):
    """Cancel a customer's subscription"""
    
    try:
        subscription = stripe.Subscription.delete(request.customer_id)
        
        return {
            "subscription_id": subscription.id,
            "status": "canceled",
            "reason": request.reason or "User cancellation"
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/webhook")
async def stripe_webhook(request: Request):
    """
    Handle Stripe webhooks
    Update your database when payments succeed, subscriptions cancel, etc.
    """
    
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, 
            sig_header, 
            os.environ.get("STRIPE_WEBHOOK_SECRET", "whsec_test_secret")
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Handle specific events
    if event["type"] == "customer.subscription.created":
        subscription = event["data"]["object"]
        print(f"✅ New subscription: {subscription['customer']}")
        # TODO: Update your database to activate user account
        
    elif event["type"] == "customer.subscription.updated":
        subscription = event["data"]["object"]
        print(f"✅ Subscription updated: {subscription['customer']}")
        # TODO: Update plan in your database
        
    elif event["type"] == "customer.subscription.deleted":
        subscription = event["data"]["object"]
        print(f"❌ Subscription canceled: {subscription['customer']}")
        # TODO: Deactivate user account
        
    elif event["type"] == "invoice.payment_succeeded":
        invoice = event["data"]["object"]
        print(f"💰 Payment received: ${invoice['amount_paid']/100}")
        # TODO: Process payment confirmation, send receipt
        
    elif event["type"] == "invoice.payment_failed":
        invoice = event["data"]["object"]
        print(f"❌ Payment failed: {invoice['customer']}")
        # TODO: Send payment failure notification, retry logic
    
    return {"status": "success"}

@router.get("/pricing")
async def get_pricing():
    """Return pricing information"""
    
    return {
        "plans": PRICING,
        "currency": "USD",
        "billing": "monthly"
    }

@router.post("/validate-coupon")
async def validate_coupon(coupon_code: str):
    """Validate a coupon code"""
    
    try:
        coupon = stripe.Coupon.retrieve(coupon_code)
        
        return {
            "valid": coupon.valid,
            "percent_off": coupon.percent_off,
            "amount_off": coupon.amount_off,
            "duration": coupon.duration
        }
    
    except stripe.error.InvalidRequestError:
        raise HTTPException(status_code=400, detail="Invalid coupon code")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_customer_subscription_status(customer_id: str):
    """Check if customer has active subscription"""
    
    subscriptions = stripe.Subscription.list(
        customer=customer_id,
        status="active"
    )
    
    return len(subscriptions.data) > 0

def upgrade_customer_plan(customer_id: str, new_plan: str):
    """Upgrade customer to a new plan"""
    
    # Get current subscription
    subscriptions = stripe.Subscription.list(customer=customer_id, status="active")
    
    if not subscriptions.data:
        raise Exception("No active subscription found")
    
    subscription = subscriptions.data[0]
    new_price = PRICING[new_plan]["price_monthly"]
    
    # Update subscription
    stripe.Subscription.modify(
        subscription.id,
        items=[{
            "id": subscription["items"]["data"][0].id,
            "price_data": {
                "currency": "usd",
                "product": subscription["items"]["data"][0].price.product,
                "unit_amount": new_price,
                "recurring": {
                    "interval": "month"
                }
            }
        }]
    )
    
    return {"status": "upgraded", "new_plan": new_plan}

# ============================================================================
# SETUP INSTRUCTIONS
# ============================================================================

"""
SETUP STEPS:

1. Create Stripe Account
   - Go to https://stripe.com
   - Sign up for free account
   - Get your API keys from Dashboard → Developers → API Keys

2. Set Environment Variables
   export STRIPE_SECRET_KEY="sk_test_..."
   export STRIPE_PUBLISHABLE_KEY="pk_test_..."
   export STRIPE_WEBHOOK_SECRET="whsec_..."

3. Install Stripe Python SDK
   pip install stripe

4. Add webhook endpoint to Stripe Dashboard
   - Dashboard → Developers → Webhooks
   - Add endpoint: https://yourdomain.com/payments/webhook
   - Select events: customer.subscription.*, invoice.payment_*

5. Update Frontend
   - Add Stripe.js to your HTML
   - Use checkout session URL from /create-checkout-session
   - Handle success/cancel redirects

6. Test Payment
   - Use test card: 4242 4242 4242 4242
   - Any future expiration date
   - Any CVC (123)

7. Monitor in Stripe Dashboard
   - Dashboard → Billing → Customers
   - Dashboard → Billing → Subscriptions
   - Dashboard → Webhooks → Event delivery

PRICING SUMMARY:
- Stripe takes 2.9% + $0.30 per transaction
- You keep 97.1% of revenue minus transaction fee
- No setup fees
- Can process unlimited transactions

EXPECTED REVENUE (from $49 Professional plan):
- Gross: $49
- Stripe fee: -$1.72
- You keep: $47.28 per customer

With 100 customers: $4,728/month
With 1,000 customers: $47,280/month

That's the power of SaaS!
"""
