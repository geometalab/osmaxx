--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: topology; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA topology;


ALTER SCHEMA topology OWNER TO postgres;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry, geography, and raster spatial types and functions';


--
-- Name: postgis_topology; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS postgis_topology WITH SCHEMA topology;


--
-- Name: EXTENSION postgis_topology; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis_topology IS 'PostGIS topology spatial types and functions';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: osmaxx; Tablespace: 
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO osmaxx;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: osmaxx
--

CREATE SEQUENCE auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO osmaxx;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: osmaxx
--

ALTER SEQUENCE auth_group_id_seq OWNED BY auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: osmaxx; Tablespace: 
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO osmaxx;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: osmaxx
--

CREATE SEQUENCE auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO osmaxx;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: osmaxx
--

ALTER SEQUENCE auth_group_permissions_id_seq OWNED BY auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: osmaxx; Tablespace: 
--

CREATE TABLE auth_permission (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO osmaxx;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: osmaxx
--

CREATE SEQUENCE auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO osmaxx;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: osmaxx
--

ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: osmaxx; Tablespace: 
--

CREATE TABLE auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone NOT NULL,
    is_superuser boolean NOT NULL,
    username character varying(30) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(75) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO osmaxx;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: osmaxx; Tablespace: 
--

CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO osmaxx;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: osmaxx
--

CREATE SEQUENCE auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO osmaxx;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: osmaxx
--

ALTER SEQUENCE auth_user_groups_id_seq OWNED BY auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: osmaxx
--

CREATE SEQUENCE auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO osmaxx;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: osmaxx
--

ALTER SEQUENCE auth_user_id_seq OWNED BY auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: osmaxx; Tablespace: 
--

CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO osmaxx;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: osmaxx
--

CREATE SEQUENCE auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO osmaxx;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: osmaxx
--

ALTER SEQUENCE auth_user_user_permissions_id_seq OWNED BY auth_user_user_permissions.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: osmaxx; Tablespace: 
--

CREATE TABLE django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO osmaxx;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: osmaxx
--

CREATE SEQUENCE django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO osmaxx;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: osmaxx
--

ALTER SEQUENCE django_admin_log_id_seq OWNED BY django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: osmaxx; Tablespace: 
--

CREATE TABLE django_content_type (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO osmaxx;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: osmaxx
--

CREATE SEQUENCE django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO osmaxx;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: osmaxx
--

ALTER SEQUENCE django_content_type_id_seq OWNED BY django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: osmaxx; Tablespace: 
--

CREATE TABLE django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO osmaxx;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: osmaxx
--

CREATE SEQUENCE django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO osmaxx;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: osmaxx
--

ALTER SEQUENCE django_migrations_id_seq OWNED BY django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: osmaxx; Tablespace: 
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO osmaxx;

--
-- Name: excerptExport_boundinggeometry; Type: TABLE; Schema: public; Owner: osmaxx; Tablespace: 
--

CREATE TABLE "excerptExport_boundinggeometry" (
    id integer NOT NULL,
    type integer NOT NULL,
    excerpt_id integer,
    geometry geometry(Geometry,4326)
);


ALTER TABLE public."excerptExport_boundinggeometry" OWNER TO osmaxx;

--
-- Name: excerptExport_boundinggeometry_id_seq; Type: SEQUENCE; Schema: public; Owner: osmaxx
--

CREATE SEQUENCE "excerptExport_boundinggeometry_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."excerptExport_boundinggeometry_id_seq" OWNER TO osmaxx;

--
-- Name: excerptExport_boundinggeometry_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: osmaxx
--

ALTER SEQUENCE "excerptExport_boundinggeometry_id_seq" OWNED BY "excerptExport_boundinggeometry".id;


--
-- Name: excerptExport_excerpt; Type: TABLE; Schema: public; Owner: osmaxx; Tablespace: 
--

CREATE TABLE "excerptExport_excerpt" (
    id integer NOT NULL,
    name character varying(128) NOT NULL,
    is_public boolean NOT NULL,
    is_active boolean NOT NULL,
    owner_id integer NOT NULL
);


ALTER TABLE public."excerptExport_excerpt" OWNER TO osmaxx;

--
-- Name: excerptExport_excerpt_id_seq; Type: SEQUENCE; Schema: public; Owner: osmaxx
--

CREATE SEQUENCE "excerptExport_excerpt_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."excerptExport_excerpt_id_seq" OWNER TO osmaxx;

--
-- Name: excerptExport_excerpt_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: osmaxx
--

ALTER SEQUENCE "excerptExport_excerpt_id_seq" OWNED BY "excerptExport_excerpt".id;


--
-- Name: excerptExport_extractionorder; Type: TABLE; Schema: public; Owner: osmaxx; Tablespace: 
--

CREATE TABLE "excerptExport_extractionorder" (
    id integer NOT NULL,
    state integer NOT NULL,
    process_start_date timestamp with time zone NOT NULL,
    process_reference character varying(128) NOT NULL,
    excerpt_id integer NOT NULL,
    orderer_id integer NOT NULL
);


ALTER TABLE public."excerptExport_extractionorder" OWNER TO osmaxx;

--
-- Name: excerptExport_extractionorder_id_seq; Type: SEQUENCE; Schema: public; Owner: osmaxx
--

CREATE SEQUENCE "excerptExport_extractionorder_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."excerptExport_extractionorder_id_seq" OWNER TO osmaxx;

--
-- Name: excerptExport_extractionorder_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: osmaxx
--

ALTER SEQUENCE "excerptExport_extractionorder_id_seq" OWNED BY "excerptExport_extractionorder".id;


--
-- Name: excerptExport_outputfile; Type: TABLE; Schema: public; Owner: osmaxx; Tablespace: 
--

CREATE TABLE "excerptExport_outputfile" (
    id integer NOT NULL,
    mime_type character varying(64) NOT NULL,
    path character varying(512) NOT NULL,
    create_date timestamp with time zone NOT NULL,
    deleted_on_filesystem boolean NOT NULL,
    extraction_order_id integer NOT NULL
);


ALTER TABLE public."excerptExport_outputfile" OWNER TO osmaxx;

--
-- Name: excerptExport_outputfile_id_seq; Type: SEQUENCE; Schema: public; Owner: osmaxx
--

CREATE SEQUENCE "excerptExport_outputfile_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."excerptExport_outputfile_id_seq" OWNER TO osmaxx;

--
-- Name: excerptExport_outputfile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: osmaxx
--

ALTER SEQUENCE "excerptExport_outputfile_id_seq" OWNED BY "excerptExport_outputfile".id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: osmaxx
--

ALTER TABLE ONLY auth_group ALTER COLUMN id SET DEFAULT nextval('auth_group_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: osmaxx
--

ALTER TABLE ONLY auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('auth_group_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: osmaxx
--

ALTER TABLE ONLY auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: osmaxx
--

ALTER TABLE ONLY auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: osmaxx
--

ALTER TABLE ONLY auth_user_groups ALTER COLUMN id SET DEFAULT nextval('auth_user_groups_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: osmaxx
--

ALTER TABLE ONLY auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('auth_user_user_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: osmaxx
--

ALTER TABLE ONLY django_admin_log ALTER COLUMN id SET DEFAULT nextval('django_admin_log_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: osmaxx
--

ALTER TABLE ONLY django_content_type ALTER COLUMN id SET DEFAULT nextval('django_content_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: osmaxx
--

ALTER TABLE ONLY django_migrations ALTER COLUMN id SET DEFAULT nextval('django_migrations_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: osmaxx
--

ALTER TABLE ONLY "excerptExport_boundinggeometry" ALTER COLUMN id SET DEFAULT nextval('"excerptExport_boundinggeometry_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: osmaxx
--

ALTER TABLE ONLY "excerptExport_excerpt" ALTER COLUMN id SET DEFAULT nextval('"excerptExport_excerpt_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: osmaxx
--

ALTER TABLE ONLY "excerptExport_extractionorder" ALTER COLUMN id SET DEFAULT nextval('"excerptExport_extractionorder_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: osmaxx
--

ALTER TABLE ONLY "excerptExport_outputfile" ALTER COLUMN id SET DEFAULT nextval('"excerptExport_outputfile_id_seq"'::regclass);


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
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: osmaxx
--

COPY auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: osmaxx
--

SELECT pg_catalog.setval('auth_group_permissions_id_seq', 1, false);


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
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: osmaxx
--

SELECT pg_catalog.setval('auth_permission_id_seq', 36, true);


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: osmaxx
--

COPY auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
2	pbkdf2_sha256$15000$eRPNPVQ7axe6$MBilaqID/YK9isxjx1dLM1ObyiQgCl0kM+I3qZFSQXg=	2015-02-27 12:33:59.87765+00	f	test				f	t	2015-02-27 12:33:59.877691+00
1	pbkdf2_sha256$15000$JNgfrf5fGxn9$DwTDPL/7buiekQhqG3bCk2mwgHdWEJ+6x53Mvn8Ge7I=	2015-02-27 13:53:23.941818+00	t	admin			admin@osmaxx.ch	t	t	2015-02-27 08:57:51.303567+00
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

SELECT pg_catalog.setval('auth_user_id_seq', 2, true);


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
1	2015-02-27 12:34:00.001253+00	2	test	1		4	1
2	2015-02-27 13:46:16.717167+00	7	Excerpt {name: Neverland}	1		9	1
3	2015-02-27 14:04:27.050712+00	5	BoundingGeometry{}	1		10	1
4	2015-02-27 14:25:43.025932+00	6	orderer: test, excerpt: Neverland	1		11	1
5	2015-02-27 14:29:36.530231+00	1	/path /to/neverland	1		12	1
\.


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: osmaxx
--

SELECT pg_catalog.setval('django_admin_log_id_seq', 5, true);


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
9	excerpt	excerptExport	excerpt
10	bounding geometry	excerptExport	boundinggeometry
11	extraction order	excerptExport	extractionorder
12	output file	excerptExport	outputfile
\.


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: osmaxx
--

SELECT pg_catalog.setval('django_content_type_id_seq', 12, true);


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: osmaxx
--

COPY django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2015-02-27 08:57:28.447577+00
2	auth	0001_initial	2015-02-27 08:57:28.552313+00
3	admin	0001_initial	2015-02-27 08:57:28.596216+00
4	excerptExport	0001_initial	2015-02-27 08:57:28.698472+00
5	excerptExport	0002_auto_20150224_1627	2015-02-27 08:57:28.791073+00
6	excerptExport	0003_auto_20150224_1703	2015-02-27 08:57:28.879449+00
7	excerptExport	0004_boundinggeometry_geometry	2015-02-27 08:57:28.953421+00
8	excerptExport	0005_auto_20150227_0748	2015-02-27 08:57:29.063244+00
9	sessions	0001_initial	2015-02-27 08:57:29.080875+00
10	excerptExport	0006_auto_20150227_1427	2015-02-27 14:28:06.420669+00
\.


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: osmaxx
--

SELECT pg_catalog.setval('django_migrations_id_seq', 10, true);


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: osmaxx
--

COPY django_session (session_key, session_data, expire_date) FROM stdin;
i6hk03rj76yys919y9jlik2whlkily9h	YWY4NmRlMmMwMTdjOThlZDBiYThmNDZlZWQxYzM1Yjc5Njg2M2Y0OTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiNjVmN2IwNzlmZGY5ODIyYzFjNDcyMjJkZGMxZTc3OTZjOWVmNzk1MSIsIl9hdXRoX3VzZXJfaWQiOjF9	2015-03-13 12:44:04.911484+00
17g48i79t4znwu3wlwttraimtha3w4mo	ZjEyN2VlZTg5NzQ3MzI3MTBjMmZmZTg5ZThjODdjZTE5ZGM1YjA5OTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MSwiX2F1dGhfdXNlcl9oYXNoIjoiNjVmN2IwNzlmZGY5ODIyYzFjNDcyMjJkZGMxZTc3OTZjOWVmNzk1MSJ9	2015-03-13 13:53:23.944227+00
\.


--
-- Data for Name: excerptExport_boundinggeometry; Type: TABLE DATA; Schema: public; Owner: osmaxx
--

COPY "excerptExport_boundinggeometry" (id, type, excerpt_id, geometry) FROM stdin;
5	0	7	\N
\.


--
-- Name: excerptExport_boundinggeometry_id_seq; Type: SEQUENCE SET; Schema: public; Owner: osmaxx
--

SELECT pg_catalog.setval('"excerptExport_boundinggeometry_id_seq"', 5, true);


--
-- Data for Name: excerptExport_excerpt; Type: TABLE DATA; Schema: public; Owner: osmaxx
--

COPY "excerptExport_excerpt" (id, name, is_public, is_active, owner_id) FROM stdin;
7	Neverland	t	t	2
\.


--
-- Name: excerptExport_excerpt_id_seq; Type: SEQUENCE SET; Schema: public; Owner: osmaxx
--

SELECT pg_catalog.setval('"excerptExport_excerpt_id_seq"', 7, true);


--
-- Data for Name: excerptExport_extractionorder; Type: TABLE DATA; Schema: public; Owner: osmaxx
--

COPY "excerptExport_extractionorder" (id, state, process_start_date, process_reference, excerpt_id, orderer_id) FROM stdin;
6	1	2015-02-27 14:25:36+00	5	7	2
\.


--
-- Name: excerptExport_extractionorder_id_seq; Type: SEQUENCE SET; Schema: public; Owner: osmaxx
--

SELECT pg_catalog.setval('"excerptExport_extractionorder_id_seq"', 6, true);


--
-- Data for Name: excerptExport_outputfile; Type: TABLE DATA; Schema: public; Owner: osmaxx
--

COPY "excerptExport_outputfile" (id, mime_type, path, create_date, deleted_on_filesystem, extraction_order_id) FROM stdin;
1	text	/path /to/neverland	2015-02-27 14:29:32+00	t	6
\.


--
-- Name: excerptExport_outputfile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: osmaxx
--

SELECT pg_catalog.setval('"excerptExport_outputfile_id_seq"', 1, true);


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


SET search_path = public, pg_catalog;

--
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: osmaxx; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions_group_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: osmaxx; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_key UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: osmaxx; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: osmaxx; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission_content_type_id_codename_key; Type: CONSTRAINT; Schema: public; Owner: osmaxx; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_key UNIQUE (content_type_id, codename);


--
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: osmaxx; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: osmaxx; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_user_id_group_id_key; Type: CONSTRAINT; Schema: public; Owner: osmaxx; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_key UNIQUE (user_id, group_id);


--
-- Name: auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: osmaxx; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: osmaxx; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_user_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: osmaxx; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_key UNIQUE (user_id, permission_id);


--
-- Name: auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: osmaxx; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: osmaxx; Tablespace: 
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type_app_label_6d1d692a86c60fa3_uniq; Type: CONSTRAINT; Schema: public; Owner: osmaxx; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_6d1d692a86c60fa3_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: osmaxx; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: osmaxx; Tablespace: 
--

ALTER TABLE ONLY django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: osmaxx; Tablespace: 
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: excerptExport_boundinggeometry_excerpt_id_key; Type: CONSTRAINT; Schema: public; Owner: osmaxx; Tablespace: 
--

ALTER TABLE ONLY "excerptExport_boundinggeometry"
    ADD CONSTRAINT "excerptExport_boundinggeometry_excerpt_id_key" UNIQUE (excerpt_id);


--
-- Name: excerptExport_boundinggeometry_pkey; Type: CONSTRAINT; Schema: public; Owner: osmaxx; Tablespace: 
--

ALTER TABLE ONLY "excerptExport_boundinggeometry"
    ADD CONSTRAINT "excerptExport_boundinggeometry_pkey" PRIMARY KEY (id);


--
-- Name: excerptExport_excerpt_pkey; Type: CONSTRAINT; Schema: public; Owner: osmaxx; Tablespace: 
--

ALTER TABLE ONLY "excerptExport_excerpt"
    ADD CONSTRAINT "excerptExport_excerpt_pkey" PRIMARY KEY (id);


--
-- Name: excerptExport_extractionorder_pkey; Type: CONSTRAINT; Schema: public; Owner: osmaxx; Tablespace: 
--

ALTER TABLE ONLY "excerptExport_extractionorder"
    ADD CONSTRAINT "excerptExport_extractionorder_pkey" PRIMARY KEY (id);


--
-- Name: excerptExport_outputfile_pkey; Type: CONSTRAINT; Schema: public; Owner: osmaxx; Tablespace: 
--

ALTER TABLE ONLY "excerptExport_outputfile"
    ADD CONSTRAINT "excerptExport_outputfile_pkey" PRIMARY KEY (id);


--
-- Name: auth_group_name_7e02d7ed75bc062_like; Type: INDEX; Schema: public; Owner: osmaxx; Tablespace: 
--

CREATE INDEX auth_group_name_7e02d7ed75bc062_like ON auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_0e939a4f; Type: INDEX; Schema: public; Owner: osmaxx; Tablespace: 
--

CREATE INDEX auth_group_permissions_0e939a4f ON auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_8373b171; Type: INDEX; Schema: public; Owner: osmaxx; Tablespace: 
--

CREATE INDEX auth_group_permissions_8373b171 ON auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_417f1b1c; Type: INDEX; Schema: public; Owner: osmaxx; Tablespace: 
--

CREATE INDEX auth_permission_417f1b1c ON auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_0e939a4f; Type: INDEX; Schema: public; Owner: osmaxx; Tablespace: 
--

CREATE INDEX auth_user_groups_0e939a4f ON auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_e8701ad4; Type: INDEX; Schema: public; Owner: osmaxx; Tablespace: 
--

CREATE INDEX auth_user_groups_e8701ad4 ON auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_8373b171; Type: INDEX; Schema: public; Owner: osmaxx; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_8373b171 ON auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_e8701ad4; Type: INDEX; Schema: public; Owner: osmaxx; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_e8701ad4 ON auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_64abb5217a0c0b32_like; Type: INDEX; Schema: public; Owner: osmaxx; Tablespace: 
--

CREATE INDEX auth_user_username_64abb5217a0c0b32_like ON auth_user USING btree (username varchar_pattern_ops);


--
-- Name: django_admin_log_417f1b1c; Type: INDEX; Schema: public; Owner: osmaxx; Tablespace: 
--

CREATE INDEX django_admin_log_417f1b1c ON django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_e8701ad4; Type: INDEX; Schema: public; Owner: osmaxx; Tablespace: 
--

CREATE INDEX django_admin_log_e8701ad4 ON django_admin_log USING btree (user_id);


--
-- Name: django_session_de54fa62; Type: INDEX; Schema: public; Owner: osmaxx; Tablespace: 
--

CREATE INDEX django_session_de54fa62 ON django_session USING btree (expire_date);


--
-- Name: django_session_session_key_25d1a855625e1585_like; Type: INDEX; Schema: public; Owner: osmaxx; Tablespace: 
--

CREATE INDEX django_session_session_key_25d1a855625e1585_like ON django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: excerptExport_boundinggeometry_geometry_id; Type: INDEX; Schema: public; Owner: osmaxx; Tablespace: 
--

CREATE INDEX "excerptExport_boundinggeometry_geometry_id" ON "excerptExport_boundinggeometry" USING gist (geometry);


--
-- Name: excerptExport_excerpt_5e7b1936; Type: INDEX; Schema: public; Owner: osmaxx; Tablespace: 
--

CREATE INDEX "excerptExport_excerpt_5e7b1936" ON "excerptExport_excerpt" USING btree (owner_id);


--
-- Name: excerptExport_extractionorder_230c0360; Type: INDEX; Schema: public; Owner: osmaxx; Tablespace: 
--

CREATE INDEX "excerptExport_extractionorder_230c0360" ON "excerptExport_extractionorder" USING btree (orderer_id);


--
-- Name: excerptExport_extractionorder_28999874; Type: INDEX; Schema: public; Owner: osmaxx; Tablespace: 
--

CREATE INDEX "excerptExport_extractionorder_28999874" ON "excerptExport_extractionorder" USING btree (excerpt_id);


--
-- Name: excerptExport_outputfile_245ededb; Type: INDEX; Schema: public; Owner: osmaxx; Tablespace: 
--

CREATE INDEX "excerptExport_outputfile_245ededb" ON "excerptExport_outputfile" USING btree (extraction_order_id);


--
-- Name: D53fef9ace6a08d93bf5bf3539521bd9; Type: FK CONSTRAINT; Schema: public; Owner: osmaxx
--

ALTER TABLE ONLY "excerptExport_outputfile"
    ADD CONSTRAINT "D53fef9ace6a08d93bf5bf3539521bd9" FOREIGN KEY (extraction_order_id) REFERENCES "excerptExport_extractionorder"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_content_type_id_34a3b14bf0e48a00_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: osmaxx
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_content_type_id_34a3b14bf0e48a00_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissio_group_id_51423762a574e157_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: osmaxx
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_group_id_51423762a574e157_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permission_id_53959fb43e1969da_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: osmaxx
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permission_id_53959fb43e1969da_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user__permission_id_6c139150877f2afe_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: osmaxx
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user__permission_id_6c139150877f2afe_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_group_id_48ee1c83ebf45d6b_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: osmaxx
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_48ee1c83ebf45d6b_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_user_id_d589d48ade01d45_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: osmaxx
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_d589d48ade01d45_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permiss_user_id_3c839064ab836e99_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: osmaxx
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permiss_user_id_3c839064ab836e99_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djan_content_type_id_1cea6f0a5c4e5f9f_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: osmaxx
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT djan_content_type_id_1cea6f0a5c4e5f9f_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_user_id_55e32449a5a1c63a_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: osmaxx
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_55e32449a5a1c63a_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: excerptE_excerpt_id_bcae1215ca879e0_fk_excerptExport_excerpt_id; Type: FK CONSTRAINT; Schema: public; Owner: osmaxx
--

ALTER TABLE ONLY "excerptExport_boundinggeometry"
    ADD CONSTRAINT "excerptE_excerpt_id_bcae1215ca879e0_fk_excerptExport_excerpt_id" FOREIGN KEY (excerpt_id) REFERENCES "excerptExport_excerpt"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: excerptExport_excerpt_owner_id_61b50617b4ae557f_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: osmaxx
--

ALTER TABLE ONLY "excerptExport_excerpt"
    ADD CONSTRAINT "excerptExport_excerpt_owner_id_61b50617b4ae557f_fk_auth_user_id" FOREIGN KEY (owner_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: excerptExport_extra_orderer_id_6d8dc67c41045671_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: osmaxx
--

ALTER TABLE ONLY "excerptExport_extractionorder"
    ADD CONSTRAINT "excerptExport_extra_orderer_id_6d8dc67c41045671_fk_auth_user_id" FOREIGN KEY (orderer_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: excerpt_excerpt_id_65d1bfbd6f6e17e3_fk_excerptExport_excerpt_id; Type: FK CONSTRAINT; Schema: public; Owner: osmaxx
--

ALTER TABLE ONLY "excerptExport_extractionorder"
    ADD CONSTRAINT "excerpt_excerpt_id_65d1bfbd6f6e17e3_fk_excerptExport_excerpt_id" FOREIGN KEY (excerpt_id) REFERENCES "excerptExport_excerpt"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

