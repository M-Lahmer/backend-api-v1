# Porject Description voir https://github.com/M-Lahmer/backend-api-v1.wiki.git

## Updates 
on accede au pod en mode sh pour executer mkdir -p /app/logs;chmod 777 /app/logs et   uvicorn main:app --host 0.0.0.0 --port 8000
```backend-deployment.yaml
  command: ["sh", "-c"]
          args:
          - |
            # Create logs directory with proper permissions
            mkdir -p /app/logs
            chmod 777 /app/logs
            # Start the application
            uvicorn main:app --host 0.0.0.0 --port 8000

