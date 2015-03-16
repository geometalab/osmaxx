--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: osmaxx
--

COPY auth_group (id, name) FROM stdin;
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: osmaxx
--

SELECT pg_catalog.setval('auth_group_id_seq', 1, false);


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: osmaxx
--

COPY django_content_type (id, name, app_label, model) FROM stdin;
1	log entry	admin	logentry
2	permission	auth	permission
3	group	auth	group
4	user	auth	user
5	content type	contenttypes	contenttype
6	session	sessions	session
7	post gis geometry columns	gis	postgisgeometrycolumns
8	post gis spatial ref sys	gis	postgisspatialrefsys
9	excerpt	excerptexport	excerpt
10	bounding geometry	excerptexport	boundinggeometry
11	extraction order	excerptexport	extractionorder
12	output file	excerptexport	outputfile
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: osmaxx
--

COPY auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can add permission	2	add_permission
5	Can change permission	2	change_permission
6	Can delete permission	2	delete_permission
7	Can add group	3	add_group
8	Can change group	3	change_group
9	Can delete group	3	delete_group
10	Can add user	4	add_user
11	Can change user	4	change_user
12	Can delete user	4	delete_user
13	Can add content type	5	add_contenttype
14	Can change content type	5	change_contenttype
15	Can delete content type	5	delete_contenttype
16	Can add session	6	add_session
17	Can change session	6	change_session
18	Can delete session	6	delete_session
19	Can add post gis geometry columns	7	add_postgisgeometrycolumns
20	Can change post gis geometry columns	7	change_postgisgeometrycolumns
21	Can delete post gis geometry columns	7	delete_postgisgeometrycolumns
22	Can add post gis spatial ref sys	8	add_postgisspatialrefsys
23	Can change post gis spatial ref sys	8	change_postgisspatialrefsys
24	Can delete post gis spatial ref sys	8	delete_postgisspatialrefsys
25	Can add excerpt	9	add_excerpt
26	Can change excerpt	9	change_excerpt
27	Can delete excerpt	9	delete_excerpt
28	Can add bounding geometry	10	add_boundinggeometry
29	Can change bounding geometry	10	change_boundinggeometry
30	Can delete bounding geometry	10	delete_boundinggeometry
31	Can add extraction order	11	add_extractionorder
32	Can change extraction order	11	change_extractionorder
33	Can delete extraction order	11	delete_extractionorder
34	Can add output file	12	add_outputfile
35	Can change output file	12	change_outputfile
36	Can delete output file	12	delete_outputfile
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: osmaxx
--

COPY auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: osmaxx
--

SELECT pg_catalog.setval('auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: osmaxx
--

SELECT pg_catalog.setval('auth_permission_id_seq', 36, true);


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: osmaxx
--

COPY auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
1	pbkdf2_sha256$15000$g6ka3dz4xWs2$dnrccGcgQYNXYpYUIIGSfA31+2wMt4qFIa/vOwzXmDY=	2015-03-10 14:21:30.210686+00	t	admin				t	t	2015-03-10 14:21:12.39213+00
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: osmaxx
--

COPY auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: osmaxx
--

SELECT pg_catalog.setval('auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: osmaxx
--

SELECT pg_catalog.setval('auth_user_id_seq', 1, true);


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: osmaxx
--

COPY auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: osmaxx
--

SELECT pg_catalog.setval('auth_user_user_permissions_id_seq', 1, false);


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: osmaxx
--

COPY django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: osmaxx
--

SELECT pg_catalog.setval('django_admin_log_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: osmaxx
--

SELECT pg_catalog.setval('django_content_type_id_seq', 12, true);


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: osmaxx
--

COPY django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2015-03-10 14:20:32.99273+00
2	auth	0001_initial	2015-03-10 14:20:33.099779+00
3	admin	0001_initial	2015-03-10 14:20:33.149468+00
4	excerptexport	0001_initial	2015-03-10 14:20:33.276293+00
5	sessions	0001_initial	2015-03-10 14:20:33.300442+00
\.


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: osmaxx
--

SELECT pg_catalog.setval('django_migrations_id_seq', 5, true);


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: osmaxx
--

COPY django_session (session_key, session_data, expire_date) FROM stdin;
3pteq1w1mu5t441ch61ga288rgvixjse	YzJmN2I5ZjMyMGRhYWRjMjAzN2I1ZTc2ODdhZmE1MjE3MzIwN2QxMDp7Il9hdXRoX3VzZXJfaWQiOjEsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiNjdlYTJlMzg3ZTQyOGIyMWI5NWRjNmQzMTI4ODM1YmI3ZDE3Yjg1YyJ9	2015-03-24 14:21:30.212299+00
\.


--
-- Data for Name: excerptexport_excerpt; Type: TABLE DATA; Schema: public; Owner: osmaxx
--

COPY excerptexport_excerpt (id, name, is_public, is_active, owner_id) FROM stdin;
1	Neverland	f	t	1
2	Rappi	t	t	1
\.


--
-- Data for Name: excerptexport_boundinggeometry; Type: TABLE DATA; Schema: public; Owner: osmaxx
--

COPY excerptexport_boundinggeometry (id, type, geometry, excerpt_id) FROM stdin;
1	0	0103000020E610000001000000050000000000000000FC52401F11A3BE66E34B400000000000FC5240BC5F5442D9A05040FFFFFFFFFF955E40BC5F5442D9A05040FFFFFFFFFF955E401F11A3BE66E34B400000000000FC52401F11A3BE66E34B40	1
2	0	0103000020E6100000010000000500000000000080B9962140F99FD751A499474000000080B99621403AD5CAA5E6A04740000000003EBF21403AD5CAA5E6A04740000000003EBF2140F99FD751A499474000000080B9962140F99FD751A4994740	2
\.


--
-- Name: excerptexport_boundinggeometry_id_seq; Type: SEQUENCE SET; Schema: public; Owner: osmaxx
--

SELECT pg_catalog.setval('excerptexport_boundinggeometry_id_seq', 2, true);


--
-- Name: excerptexport_excerpt_id_seq; Type: SEQUENCE SET; Schema: public; Owner: osmaxx
--

SELECT pg_catalog.setval('excerptexport_excerpt_id_seq', 2, true);


--
-- Data for Name: excerptexport_extractionorder; Type: TABLE DATA; Schema: public; Owner: osmaxx
--

COPY excerptexport_extractionorder (id, state, process_start_date, process_reference, excerpt_id, orderer_id) FROM stdin;
\.


--
-- Name: excerptexport_extractionorder_id_seq; Type: SEQUENCE SET; Schema: public; Owner: osmaxx
--

SELECT pg_catalog.setval('excerptexport_extractionorder_id_seq', 1, false);


--
-- Data for Name: excerptexport_outputfile; Type: TABLE DATA; Schema: public; Owner: osmaxx
--

COPY excerptexport_outputfile (id, mime_type, path, create_date, deleted_on_filesystem, extraction_order_id) FROM stdin;
\.


--
-- Name: excerptexport_outputfile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: osmaxx
--

SELECT pg_catalog.setval('excerptexport_outputfile_id_seq', 1, false);


--
-- Data for Name: spatial_ref_sys; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY spatial_ref_sys (srid, auth_name, auth_srid, srtext, proj4text) FROM stdin;
\.


SET search_path = topology, pg_catalog;

--
-- Data for Name: layer; Type: TABLE DATA; Schema: topology; Owner: postgres
--

COPY layer (topology_id, layer_id, schema_name, table_name, feature_column, feature_type, level, child_id) FROM stdin;
\.


--
-- Data for Name: topology; Type: TABLE DATA; Schema: topology; Owner: postgres
--

COPY topology (id, name, srid, "precision", hasz) FROM stdin;
\.


--
-- PostgreSQL database dump complete
--

