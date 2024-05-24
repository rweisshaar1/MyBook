-- Insert users and return their IDs
  INSERT INTO users (email, username, password, first_name, last_name, created_at, updated_at)
  VALUES 
  ('demo1@example.com', 'demo1', 'pbkdf2:sha256:600000$9JBha6PYXvqllT4r$62df4b70328de2fdcb327b054783a6a6ebc937a174b179bbe9684741dec82351', 'Demo', 'User1', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  ('demo2@example.com', 'your_friend', 'pbkdf2:sha256:600000$k2Chg8MivObv4Sln$6964afd4f15351b144f91d3c44a1ec2a3afa4bed8f80accc02908ade9f76b711', 'Friend', 'User2', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
-- demo1 password: password1
-- your_friend password: password2

