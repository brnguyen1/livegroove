# livegroove

## Backend
### Local Testing
```
python3 backend.py
```

### Deployment
```
gunicorn backend:app
```

## Frontend
### Local Testing
``` 
npm install;
npm run dev;
```

### Deployment
```
npm run build
```
### Environment Vars
```
VITE_BACKEND_URL=<local/production URL>

```

## For requirements
pip install -r requirements.txt
