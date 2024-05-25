CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Status: Want to Read, Reading, Read, Favorite
CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    book_id TEXT NOT NULL,
    image TEXT,
    title VARCHAR(255) NOT NULL,
    author TEXT,
    genre TEXT,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    rating INT DEFAULT 0,
    user_rating INT DEFAULT 0,
    comment TEXT,
    status TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- incorperate a friends table?
-- Status: Pending, Accepted, Declined, Blocked, Unfollowed
CREATE TABLE IF NOT EXISTS friends (
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    friend_id INT REFERENCES users(id) ON DELETE CASCADE,
    status TEXT DEFAULT 'Pending',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, friend_id)
);