# # Backend Dockerfile (Django example)

# # Step 1: Use a base Python image
# FROM python:3.10-slim

# # Step 2: Set working directory inside the container
# WORKDIR /app

# # Step 3: Copy the requirements.txt file
# COPY requirements.txt ./

# # Step 4: Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Step 5: Copy the rest of the backend source code
# COPY . .

# # Step 6: Run database migrations and collect static files (if needed)
# RUN python manage.py migrate
# RUN python manage.py collectstatic --noinput

# # Expose the port the Django app runs on
# EXPOSE 8000

# # Step 7: Start the Django app
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


FROM python:3.9-slim
WORKDIR /app 
COPY requirements.txt . 
RUN pip install -r requirements.txt 
COPY . . 
EXPOSE 5000 
CMD ["python", "app.py"]