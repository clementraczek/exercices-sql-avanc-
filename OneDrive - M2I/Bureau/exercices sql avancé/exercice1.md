

## 1. Catalogue public des morceaux

```sql
CREATE OR REPLACE VIEW infos_tracks AS
SELECT 
	t.track_id,
	t.title,
	t.duration_s,
	a.name
from tracks as t
join artists as a
on t.artist_id = a.artist_id;

SELECT * 
FROM infos_tracks
order by name;




## 2. Utilisateurs Premium français



CREATE OR REPLACE VIEW infos_users AS
SELECT 
	user_id,
	username,
	country,
	subscription
from users
where country='France' and subscription='Premium';

select * from infos_users
order by username;
---

## 3. Historique détaillé des écoutes



CREATE OR REPLACE VIEW histo_ecoutes AS
SELECT 
    u.user_id,
    u.username,
    u.country,
    t.title,
    a.name AS artist_name,
    l.listened_at,
    l.seconds_played
FROM listenings AS l
JOIN users AS u
    ON l.user_id = u.user_id
JOIN tracks AS t
    ON l.track_id = t.track_id
JOIN artists AS a
    ON t.artist_id = a.artist_id;

select * from histo_ecoutes;
	




---

## 4. Statistiques d’écoute par artiste


CREATE MATERIALIZED VIEW stats_artistes AS
SELECT
    a.artist_id,
    a.name AS artist_name,
    COUNT(*) AS nb_ecoutes,
    SUM(l.seconds_played) AS total_seconds,
    ROUND(AVG(l.seconds_played), 2) AS avg_seconds
FROM listenings l
JOIN tracks t
    ON l.track_id = t.track_id
JOIN artists a
    ON t.artist_id = a.artist_id
GROUP BY a.artist_id, a.name;


SELECT *
FROM stats_artistes
ORDER BY nb_ecoutes DESC;

SELECT *
FROM stats_artistes
ORDER BY total_seconds DESC;


---

## 5. Analyse par pays d’artiste


SELECT
    a.country,
    SUM(sa.total_seconds) AS total_seconds_country,
    COUNT(sa.artist_id) AS nb_artistes
FROM stats_artistes sa
JOIN artists a
    ON sa.artist_id = a.artist_id
GROUP BY a.country
ORDER BY total_seconds_country DESC;

---

## 6. Optimisation et index

