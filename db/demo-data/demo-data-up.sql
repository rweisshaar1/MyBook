-- Insert users and return their IDs
  INSERT INTO users (email, username, password, first_name, last_name, created_at, updated_at)
  VALUES 
  ('demo1@example.com', 'demo1', 'password1', 'Demo', 'User1', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('demo2@example.com', 'your_friend', 'password2', 'Friend', 'User2', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)

