-- Migration: Add user_preferences table
-- Run this in Supabase SQL Editor

CREATE TABLE IF NOT EXISTS user_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Preference categories
    preferred_language VARCHAR(10) DEFAULT 'en',
    preferred_tone VARCHAR(50) DEFAULT 'friendly',
    topics_of_interest JSONB DEFAULT '[]'::jsonb,
    
    -- Context tracking
    conversation_style VARCHAR(50) DEFAULT 'balanced',
    response_length VARCHAR(20) DEFAULT 'medium',
    
    -- User profile
    name VARCHAR(100),
    timezone VARCHAR(50),
    custom_context TEXT,
    
    -- Metadata
    preferences_json JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Constraints
    UNIQUE(user_id)
);

-- Create index for faster lookups
CREATE INDEX IF NOT EXISTS idx_user_preferences_user_id ON user_preferences(user_id);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_user_preferences_updated_at 
    BEFORE UPDATE ON user_preferences 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Grant permissions (adjust as needed)
ALTER TABLE user_preferences ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only access their own preferences
CREATE POLICY user_preferences_policy ON user_preferences
    FOR ALL
    USING (auth.uid() = user_id);
