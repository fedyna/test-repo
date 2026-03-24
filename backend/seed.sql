INSERT INTO clusters (cluster_id, name, seed_keywords, description) VALUES
(1, 'n8n use cases', '["n8n","workflow","self-host"]', 'Integrations/workflows with n8n'),
(2, 'agents/code', '["claude code","codex","agent","agentic"]', 'Coding agents and autonomous workflows'),
(3, 'prompting/methodology', '["prompt","evaluation","benchmark"]', 'Prompting frameworks and methods'),
(4, 'integrations/tools', '["zapier","make","activepieces","db","traefik"]', 'Toolchain integrations'),
(5, 'business ROI', '["roi","cost","time saving","ops"]', 'Business impact and automation ROI'),
(6, 'news/releases', '["release","update","model","comparison"]', 'AI tooling release and comparisons')
ON CONFLICT DO NOTHING;

INSERT INTO settings (key, value) VALUES
('timezone_ru', '"Europe/Moscow"'),
('timezone_us', '"America/Los_Angeles"'),
('run_times_ru', '["08:00", "20:00"]'),
('run_times_us', '["08:00", "20:00"]'),
('keywords_ru', '["claude code","openai codex","агенты","автоматизация","n8n"]'),
('keywords_en', '["claude code","openai codex","ai agents","agentic workflows","automation"]'),
('max_channels_per_region', '50'),
('max_recent_videos_per_channel', '50'),
('windows_hours', '[24,48,72,168]'),
('scoring_weights', '{"w1":0.45,"w2":0.30,"w3":0.15,"w4":0.10}'),
('thresholds', '{"min_score":0.5,"min_published_days":20,"min_delta_views":100}')
ON CONFLICT DO NOTHING;
