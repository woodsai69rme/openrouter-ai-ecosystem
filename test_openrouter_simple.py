import os
import requests

# Test OpenRouter connection
api_key = os.environ.get('OPENROUTER_API_KEY', 'NOT_SET')

print('🧪 OPENROUTER CONNECTION TEST')
print('=' * 30)

if api_key == 'NOT_SET':
    print('❌ OPENROUTER_API_KEY not set!')
    exit(1)

print(f'✅ API Key: {api_key[:10]}...')

# Test primary free models
models = [
    'openai/gpt-oss-20b:free',
    'z-ai/glm-4.5-air:free', 
    'deepseek/deepseek-r1:free'
]

print('\n🚀 Testing Free Models:')
success = 0

for model in models:
    try:
        response = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers={'Authorization': f'Bearer {api_key}'},
            json={
                'model': model,
                'messages': [{'role': 'user', 'content': 'hi'}],
                'max_tokens': 5
            },
            timeout=10
        )
        
        if response.status_code == 200:
            print(f'✅ {model}: Working')
            success += 1
        else:
            print(f'❌ {model}: HTTP {response.status_code}')
    except:
        print(f'❌ {model}: Connection error')

print(f'\n📊 Results: {success}/{len(models)} models working')
print(f'💰 Cost: $0.00 (all free models)')

if success >= 2:
    print('🎉 OpenRouter operational!')
else:
    print('⚠️ Check configuration')