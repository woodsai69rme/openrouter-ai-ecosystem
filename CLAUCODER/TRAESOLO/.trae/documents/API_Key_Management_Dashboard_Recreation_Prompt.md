# API Key Management Dashboard - Complete Recreation Prompt

## Project Overview
Create a comprehensive API Key Management Dashboard for developers to manage, monitor, and rotate API keys across multiple AI providers. The dashboard should provide real-time usage tracking, free tier monitoring, one-click clipboard functionality, and integrated access to provider documentation.

## Core Requirements

### 1. Multi-Provider Support
Support the following AI providers with dedicated integration:
- **OpenAI** (GPT models, DALL-E, Whisper)
- **Anthropic** (Claude models)
- **Google Gemini** (Gemini Pro, Gemini Vision)
- **OpenRouter** (Unified AI model access)
- **GitHub** (Copilot, Actions)
- **Qwen** (Alibaba's AI models)
- **Additional providers**: Cohere, Hugging Face, Replicate

### 2. Key Management Features
- **Add/Edit/Delete Keys**: Secure form-based key management
- **Key Rotation**: Automated and manual rotation with backup keys
- **One-Click Copy**: Instant clipboard copying with visual feedback
- **Key Validation**: Test key validity against provider APIs
- **Encryption**: Client-side encryption before storage
- **Expiration Tracking**: Monitor key expiration dates

### 3. Usage Monitoring
- **Real-time Tracking**: Live usage updates via WebSocket
- **Free Tier Limits**: Track usage against free tier quotas
- **Cost Calculation**: Estimate costs based on usage patterns
- **Rate Limit Monitoring**: Track and alert on rate limits
- **Historical Analytics**: Charts and graphs for usage trends
- **Alert System**: Configurable alerts for thresholds

### 4. User Interface Requirements

#### Dashboard Home Page
```
┌─────────────────────────────────────────────────────────────┐
│ API Key Management Dashboard                    [Settings] │
├─────────────────────────────────────────────────────────────┤
│ Quick Stats                                                 │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐           │
│ │ Active  │ │ Total   │ │ Usage   │ │ Alerts  │           │
│ │ Keys: 8 │ │ Usage   │ │ Today   │ │ 2 Active│           │
│ │         │ │ $12.45  │ │ 15.2K   │ │         │           │
│ └─────────┘ └─────────┘ └─────────┘ └─────────┘           │
├─────────────────────────────────────────────────────────────┤
│ Provider Keys                                               │
│ ┌─OpenAI──────────┐ ┌─Anthropic──────┐ ┌─Google─────────┐ │
│ │ ●Active         │ │ ●Active        │ │ ⚠️Limited      │ │
│ │ Usage: 45%      │ │ Usage: 23%     │ │ Usage: 95%     │ │
│ │ [Copy] [Rotate] │ │ [Copy] [Rotate]│ │ [Copy] [Rotate]│ │
│ └─────────────────┘ └────────────────┘ └────────────────┘ │
│ ┌─OpenRouter──────┐ ┌─GitHub─────────┐ ┌─Qwen───────────┐ │
│ │ ●Active         │ │ ●Active        │ │ ●Active        │ │
│ │ Usage: 12%      │ │ Usage: 67%     │ │ Usage: 8%      │ │
│ │ [Copy] [Rotate] │ │ [Copy] [Rotate]│ │ [Copy] [Rotate]│ │
│ └─────────────────┘ └────────────────┘ └────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

#### Key Management Interface
- **Provider Tabs**: Separate tabs for each provider
- **Add Key Form**: Secure input with validation
- **Key List**: Table with status, usage, and actions
- **Bulk Operations**: Select multiple keys for batch actions

#### Usage Analytics Page
- **Real-time Charts**: Live updating usage graphs
- **Cost Breakdown**: Per-provider cost analysis
- **Usage Patterns**: Daily/weekly/monthly trends
- **Optimization Tips**: Suggestions for cost reduction

### 5. Technical Implementation

#### Frontend Stack
```typescript
// Required Dependencies
{
  "react": "^18.2.0",
  "typescript": "^5.0.0",
  "vite": "^4.4.0",
  "tailwindcss": "^3.3.0",
  "@supabase/supabase-js": "^2.38.0",
  "zustand": "^4.4.0",
  "chart.js": "^4.4.0",
  "react-chartjs-2": "^5.2.0",
  "lucide-react": "^0.263.0",
  "react-hot-toast": "^2.4.0",
  "crypto-js": "^4.1.1"
}
```

#### Core Components Structure
```
src/
├── components/
│   ├── Dashboard/
│   │   ├── StatsPanel.tsx
│   │   ├── KeyGrid.tsx
│   │   └── QuickActions.tsx
│   ├── KeyManagement/
│   │   ├── AddKeyForm.tsx
│   │   ├── KeyList.tsx
│   │   └── KeyRotation.tsx
│   ├── Analytics/
│   │   ├── UsageChart.tsx
│   │   ├── CostBreakdown.tsx
│   │   └── AlertsPanel.tsx
│   └── Providers/
│       ├── ProviderCard.tsx
│       ├── ProviderLinks.tsx
│       └── IntegrationGuide.tsx
├── hooks/
│   ├── useApiKeys.ts
│   ├── useUsageTracking.ts
│   └── useClipboard.ts
├── stores/
│   ├── keyStore.ts
│   ├── usageStore.ts
│   └── settingsStore.ts
├── utils/
│   ├── encryption.ts
│   ├── providers.ts
│   └── validation.ts
└── types/
    ├── api.ts
    ├── providers.ts
    └── usage.ts
```

#### Key Store Implementation
```typescript
import { create } from 'zustand';
import { supabase } from '../lib/supabase';
import { encryptKey, decryptKey } from '../utils/encryption';

interface ApiKey {
  id: string;
  provider: string;
  name: string;
  encryptedKey: string;
  status: 'active' | 'inactive' | 'expired' | 'limited';
  usageLimit?: number;
  currentUsage: number;
  expiresAt?: Date;
  createdAt: Date;
}

interface KeyStore {
  keys: ApiKey[];
  loading: boolean;
  addKey: (provider: string, name: string, key: string) => Promise<void>;
  updateKey: (id: string, updates: Partial<ApiKey>) => Promise<void>;
  deleteKey: (id: string) => Promise<void>;
  rotateKey: (id: string, newKey: string) => Promise<void>;
  copyToClipboard: (id: string) => Promise<void>;
  fetchKeys: () => Promise<void>;
}

export const useKeyStore = create<KeyStore>((set, get) => ({
  keys: [],
  loading: false,
  
  addKey: async (provider, name, key) => {
    set({ loading: true });
    try {
      const encryptedKey = encryptKey(key);
      const { data, error } = await supabase
        .from('api_keys')
        .insert({
          provider,
          name,
          encrypted_key: encryptedKey,
          status: 'active'
        })
        .select()
        .single();
      
      if (error) throw error;
      
      set(state => ({
        keys: [...state.keys, data],
        loading: false
      }));
    } catch (error) {
      console.error('Error adding key:', error);
      set({ loading: false });
    }
  },
  
  copyToClipboard: async (id) => {
    const key = get().keys.find(k => k.id === id);
    if (!key) return;
    
    try {
      const decryptedKey = decryptKey(key.encryptedKey);
      await navigator.clipboard.writeText(decryptedKey);
      // Show success toast
    } catch (error) {
      console.error('Error copying to clipboard:', error);
    }
  },
  
  // ... other methods
}));
```

#### Provider Configuration
```typescript
export const PROVIDERS = {
  openai: {
    name: 'OpenAI',
    logo: '/logos/openai.svg',
    color: '#00A67E',
    getKeyUrl: 'https://platform.openai.com/api-keys',
    docsUrl: 'https://platform.openai.com/docs',
    testEndpoint: 'https://api.openai.com/v1/models',
    freeLimit: { tokens: 100000, period: 'month' },
    keyFormat: /^sk-[A-Za-z0-9]{48}$/
  },
  anthropic: {
    name: 'Anthropic',
    logo: '/logos/anthropic.svg',
    color: '#D4A574',
    getKeyUrl: 'https://console.anthropic.com/account/keys',
    docsUrl: 'https://docs.anthropic.com',
    testEndpoint: 'https://api.anthropic.com/v1/messages',
    freeLimit: { tokens: 50000, period: 'month' },
    keyFormat: /^sk-ant-[A-Za-z0-9-_]{95}$/
  },
  google: {
    name: 'Google Gemini',
    logo: '/logos/google.svg',
    color: '#4285F4',
    getKeyUrl: 'https://makersuite.google.com/app/apikey',
    docsUrl: 'https://ai.google.dev/docs',
    testEndpoint: 'https://generativelanguage.googleapis.com/v1/models',
    freeLimit: { requests: 60, period: 'minute' },
    keyFormat: /^AIza[A-Za-z0-9_-]{35}$/
  },
  openrouter: {
    name: 'OpenRouter',
    logo: '/logos/openrouter.svg',
    color: '#8B5CF6',
    getKeyUrl: 'https://openrouter.ai/keys',
    docsUrl: 'https://openrouter.ai/docs',
    testEndpoint: 'https://openrouter.ai/api/v1/models',
    freeLimit: { credits: 10, period: 'month' },
    keyFormat: /^sk-or-[A-Za-z0-9-_]{43}$/
  },
  github: {
    name: 'GitHub',
    logo: '/logos/github.svg',
    color: '#24292E',
    getKeyUrl: 'https://github.com/settings/tokens',
    docsUrl: 'https://docs.github.com/en/rest',
    testEndpoint: 'https://api.github.com/user',
    keyFormat: /^gh[ps]_[A-Za-z0-9]{36}$/
  },
  qwen: {
    name: 'Qwen',
    logo: '/logos/qwen.svg',
    color: '#FF6B35',
    getKeyUrl: 'https://dashscope.aliyun.com',
    docsUrl: 'https://help.aliyun.com/zh/dashscope',
    testEndpoint: 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation',
    keyFormat: /^sk-[A-Za-z0-9]{32}$/
  }
};
```

### 6. Real-time Features

#### WebSocket Usage Tracking
```typescript
import { useEffect } from 'react';
import { supabase } from '../lib/supabase';
import { useUsageStore } from '../stores/usageStore';

export const useRealtimeUsage = () => {
  const { updateUsage } = useUsageStore();
  
  useEffect(() => {
    const channel = supabase
      .channel('usage_updates')
      .on(
        'postgres_changes',
        {
          event: 'INSERT',
          schema: 'public',
          table: 'usage_records'
        },
        (payload) => {
          updateUsage(payload.new);
        }
      )
      .subscribe();
    
    return () => {
      supabase.removeChannel(channel);
    };
  }, [updateUsage]);
};
```

### 7. Security Features

#### Client-side Encryption
```typescript
import CryptoJS from 'crypto-js';

const ENCRYPTION_KEY = process.env.VITE_ENCRYPTION_KEY || 'default-key';

export const encryptKey = (key: string): string => {
  return CryptoJS.AES.encrypt(key, ENCRYPTION_KEY).toString();
};

export const decryptKey = (encryptedKey: string): string => {
  const bytes = CryptoJS.AES.decrypt(encryptedKey, ENCRYPTION_KEY);
  return bytes.toString(CryptoJS.enc.Utf8);
};
```

### 8. Deployment Configuration

#### Environment Variables
```env
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
VITE_ENCRYPTION_KEY=your_encryption_key
VITE_APP_URL=your_app_url
```

#### Vercel Configuration
```json
{
  "framework": "vite",
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "installCommand": "npm install",
  "devCommand": "npm run dev"
}
```

### 9. Additional Features

#### Provider Integration Links
- **Quick Access**: Direct links to provider dashboards
- **Documentation**: Embedded integration guides
- **Pricing**: Real-time pricing information
- **Status**: Provider service status monitoring

#### Team Collaboration
- **Shared Keys**: Team-based key sharing
- **Permissions**: Role-based access control
- **Audit Logs**: Track key usage by team members
- **Billing**: Consolidated usage reporting

#### Export/Import
- **Backup**: Export key configurations
- **Migration**: Import from other tools
- **Sync**: Cross-device synchronization

### 10. Testing Requirements

#### Unit Tests
- Key encryption/decryption
- Provider validation
- Usage calculations
- Clipboard functionality

#### Integration Tests
- Supabase operations
- Real-time updates
- Provider API calls
- Authentication flows

### 11. Documentation Requirements

#### User Documentation
- Setup guide for each provider
- Usage tracking explanation
- Security best practices
- Troubleshooting guide

#### Developer Documentation
- API reference
- Component documentation
- Deployment guide
- Contributing guidelines

## Implementation Priority

1. **Phase 1**: Basic key management and storage
2. **Phase 2**: Provider integration and validation
3. **Phase 3**: Usage tracking and analytics
4. **Phase 4**: Real-time features and alerts
5. **Phase 5**: Team collaboration and advanced features

## Success Metrics

- **Functionality**: All providers working correctly
- **Performance**: Sub-100ms clipboard operations
- **Security**: Encrypted storage and secure transmission
- **Usability**: Intuitive interface with minimal clicks
- **Reliability**: 99.9% uptime for key operations

This recreation prompt provides a comprehensive foundation for building a professional-grade API Key Management Dashboard that meets all specified requirements while maintaining security, performance, and usability standards.