# Marketplace & Derivative Creation Feature

## Overview

The marketplace feature enables creators to:
1. **Publish** their semantic blueprints to a public gallery
2. **Purchase credits** to use other creators' blueprints
3. **Create derivatives** from purchased blueprints
4. **Track derivative chains** showing the lineage of content
5. **Earn revenue** when others use their blueprints

## User Flow

### For Blueprint Creators

1. **Upload & Generate Blueprint**
   - Upload comic book (or any content)
   - Generate semantic JSON blueprint
   - Register on Story Protocol

2. **Publish to Marketplace**
   - Navigate to marketplace
   - Click "List Blueprint"
   - Set title, description, price (in credits)
   - Add tags and category
   - Publish listing

3. **Monitor Usage**
   - See how many users purchased blueprint
   - View all derivatives created from blueprint
   - Track revenue from sales and derivative creation
   - See derivative chain visualization

### For Derivative Creators

1. **Browse Marketplace**
   - Explore public gallery of semantic blueprints
   - Filter by category, tags, price
   - Preview blueprint details and semantic fingerprint
   - View derivative chain (see what others created)

2. **Purchase Credits** (if needed)
   - Navigate to credits page
   - Select credit package
   - Complete payment
   - Credits added to account

3. **Purchase Blueprint**
   - Click "Use This Blueprint" on listing
   - Confirm credit deduction
   - Receive access token
   - Blueprint unlocked for use

4. **Create Derivative**
   - Click "Create Derivative" on purchased blueprint
   - Configure regeneration parameters:
     - Target format (comic → animation script, etc.)
     - Style adaptation
     - Cultural localization
     - Length adaptation
   - Start generation process
   - **Automatic Story Protocol Registration**:
     - Derivative content generated
     - New semantic fingerprint created
     - Registered on Story Protocol with parent relationship
     - Derivative appears in gallery with attribution

5. **View Derivative Chain**
   - See: Original → Your Derivative → Sub-derivatives
   - Track full lineage
   - View all content in the chain

## Derivative Chain Example

```
Original Comic Book (Creator A)
  └── Semantic Blueprint A (Listed on Marketplace)
      └── Derivative 1: Animation Script (Creator B)
          └── Derivative 2: Short Story (Creator C)
              └── Derivative 3: Comic Adaptation (Creator D)
```

Each derivative:
- Is registered on Story Protocol with parent relationship
- Shows attribution chain
- Can generate revenue for parent creators
- Appears in marketplace (if creator chooses to list it)

## Story Protocol Integration

### Registration Flow

1. **Original Content**
   - Register semantic blueprint as IP Asset
   - Mint NFT representing ownership
   - Store on IPFS

2. **Derivative Creation**
   - Generate derivative content from parent blueprint
   - Create new semantic fingerprint for derivative
   - Register derivative on Story Protocol:
     - Link to parent IP Asset
     - Establish derivative relationship
     - Mint derivative NFT
     - Store derivative fingerprint on IPFS
   - Update derivative chain in database

### Parent-Child Relationships

Story Protocol tracks:
- Original IP Asset ID
- Parent IP Asset ID (for derivatives)
- Derivative relationships
- Attribution chain
- Ownership and licensing

## Credit System

### Credit Packages

- **Starter**: 10 credits - $5
- **Creator**: 50 credits - $20
- **Pro**: 200 credits - $75
- **Enterprise**: 1000 credits - $300

### Credit Usage

- **Blueprint Purchase**: Varies by creator pricing (1-50 credits typical)
- **Derivative Creation**: 5 credits per derivative
- **Advanced Features**: Additional credits for premium tools

### Revenue Sharing

When a derivative is created:
- **Original Creator**: Earns 30% of blueprint purchase price
- **Intermediate Creators**: Earn 10% if their derivative is used
- **Platform**: Takes 20% fee
- **Derivative Creator**: Keeps 40% if they list their derivative

## Database Schema

See `TECHNICAL-SPEC.md` for complete schema. Key tables:
- `marketplace_listings` - Public blueprint listings
- `credit_balances` - User credit accounts
- `credit_transactions` - Credit purchase/spend history
- `derivatives` - Derivative content tracking
- `revenue_shares` - Revenue distribution
- `marketplace_purchases` - Purchase records

## API Endpoints

### Marketplace

```
GET    /api/marketplace
  - Browse listings with filters
  - Returns: { listings: [...], pagination }

GET    /api/marketplace/:id
  - Get listing details
  - Returns: { listing, fingerprint_preview, derivative_count }

POST   /api/marketplace/list
  - Create new listing
  - Body: { fingerprint_id, title, price_credits, ... }

POST   /api/marketplace/:id/purchase
  - Purchase blueprint access
  - Deducts credits
  - Returns: { access_token, credits_remaining }
```

### Derivatives

```
POST   /api/marketplace/:listingId/create-derivative
  - Create derivative from purchased blueprint
  - Body: { regeneration_type, target_format, parameters }
  - Returns: { job_id, derivative_id }
  - Automatically registers on Story Protocol

GET    /api/derivatives/:id/chain
  - Get full derivative chain
  - Returns: { chain: [...], depth, total_derivatives }
```

### Credits

```
GET    /api/credits/balance
  - Get user credit balance
  - Returns: { balance, total_earned, total_spent }

POST   /api/credits/purchase
  - Purchase credit package
  - Body: { package_id, payment_method }
  - Returns: { transaction_id, new_balance }
```

## Frontend Components

### Marketplace Page

- **GalleryGrid**: Grid view of marketplace listings
- **BlueprintCard**: Individual listing card with preview
- **Filters**: Category, price, tags, search
- **Sorting**: Popular, newest, price, derivative count

### Blueprint Details

- **BlueprintViewer**: Interactive semantic fingerprint preview
- **DerivativeChain**: Visual chain visualization
- **PurchaseButton**: Buy blueprint with credits
- **CreateDerivativeButton**: Start derivative creation

### Derivative Creation

- **CreateDerivativeForm**: Configure regeneration parameters
- **ParameterSelector**: Format, style, adaptation options
- **ProgressTracker**: Generation progress
- **StoryRegistrationStatus**: Blockchain registration status

### Credits

- **CreditBalance**: Display current balance
- **CreditPurchase**: Package selection and payment
- **TransactionHistory**: Credit transaction log

## Revenue Flow

1. **User purchases credits** → Platform receives payment
2. **User buys blueprint** → Credits deducted, creator earns share
3. **User creates derivative** → Credits deducted, parent creators earn shares
4. **Derivative listed** → Can generate revenue for derivative creator

## Attribution & Licensing

- All derivatives show full attribution chain
- Original creator always credited
- Story Protocol tracks relationships on-chain
- Licensing terms set by blueprint creator
- Derivative creators can set their own terms for their derivatives

## Future Enhancements

- **Collaborative Creation**: Multiple creators work on same blueprint
- **Royalty System**: Ongoing royalties for derivative usage
- **License Templates**: Pre-defined licensing options
- **Derivative Marketplace**: Dedicated section for derivative content
- **Social Features**: Comments, ratings, follows

