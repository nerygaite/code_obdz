delete from entries;

insert into entries(date, title, content) values (now() - interval '10 days', 'third post', 'This is my first post.  It is exciting!');
insert into entries(date, title, content) values (now() - interval '1 day', 'second post', 'I am finding Flask incredibly fun.');
insert into entries(title, content) values ('first post', 'My name is Maria from SAD-21 and I love creating websites!');
