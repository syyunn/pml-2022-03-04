CREATE TABLE company_disambiguated as
(
select url, array_agg(name) from company
group by url
order by url desc
)

alter table company_disambiguated add primary key (url);

create table stock(
name text,
url text,
price numeric,
foreign key (url) references company_disambiguated (url)
)

INSERT INTO stock (name, url, price) VALUES ('apple', 'https://www.apple.com/', 163)

INSERT INTO stock (name, url, price) VALUES ('apple', 'https://www.applebees.com/en', 69.22)

-- INSERT INTO stock (name, url, price) VALUES ('apple', 'https://www.apple.com', 163) -- should return error
-- INSERT INTO company_disambiguated (url, array_agg) VALUES ('https://www.apple.com/', '{test1, test2}') -- should return error
