--
-- PostgreSQL database dump
--

-- Dumped from database version 9.0.4
-- Dumped by pg_dump version 9.0.4
-- Started on 2011-08-26 14:46:47

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

--
-- TOC entry 315 (class 2612 OID 11574)
-- Name: plpgsql; Type: PROCEDURAL LANGUAGE; Schema: -; Owner: -
--

CREATE PROCEDURAL LANGUAGE plpgsql;
CREATE OR REPLACE PROCEDURAL LANGUAGE plpgsql;


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 1510 (class 1259 OID 16418)
-- Dependencies: 1791 1792 1793 1794 5
-- Name: entries; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE entries (
    id integer NOT NULL,
    created timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    title text DEFAULT ''::text NOT NULL,
    url text DEFAULT ''::text NOT NULL,
    text text DEFAULT ''::text NOT NULL
);


--
-- TOC entry 1511 (class 1259 OID 16459)
-- Dependencies: 5
-- Name: entries__tags; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE entries__tags (
    entry_id integer NOT NULL,
    tag_id integer NOT NULL
);


--
-- TOC entry 1509 (class 1259 OID 16416)
-- Dependencies: 5 1510
-- Name: entries_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE entries_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 1809 (class 0 OID 0)
-- Dependencies: 1509
-- Name: entries_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE entries_id_seq OWNED BY entries.id;


--
-- TOC entry 1508 (class 1259 OID 16395)
-- Dependencies: 5
-- Name: tags; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE tags (
    id integer NOT NULL,
    name text NOT NULL
);


--
-- TOC entry 1507 (class 1259 OID 16393)
-- Dependencies: 5 1508
-- Name: tags_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE tags_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 1810 (class 0 OID 0)
-- Dependencies: 1507
-- Name: tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE tags_id_seq OWNED BY tags.id;


--
-- TOC entry 1790 (class 2604 OID 16421)
-- Dependencies: 1510 1509 1510
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE entries ALTER COLUMN id SET DEFAULT nextval('entries_id_seq'::regclass);


--
-- TOC entry 1789 (class 2604 OID 16398)
-- Dependencies: 1508 1507 1508
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE tags ALTER COLUMN id SET DEFAULT nextval('tags_id_seq'::regclass);


--
-- TOC entry 1802 (class 2606 OID 16475)
-- Dependencies: 1511 1511 1511
-- Name: entries__tags_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY entries__tags
    ADD CONSTRAINT entries__tags_pkey PRIMARY KEY (entry_id, tag_id);


--
-- TOC entry 1800 (class 2606 OID 16423)
-- Dependencies: 1510 1510
-- Name: entries_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY entries
    ADD CONSTRAINT entries_pkey PRIMARY KEY (id);


--
-- TOC entry 1796 (class 2606 OID 16403)
-- Dependencies: 1508 1508
-- Name: tags_name_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY tags
    ADD CONSTRAINT tags_name_key UNIQUE (name);


--
-- TOC entry 1798 (class 2606 OID 16415)
-- Dependencies: 1508 1508
-- Name: tags_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY tags
    ADD CONSTRAINT tags_pkey PRIMARY KEY (id);


--
-- TOC entry 1803 (class 2606 OID 16464)
-- Dependencies: 1799 1511 1510
-- Name: entries__tags_entry_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY entries__tags
    ADD CONSTRAINT entries__tags_entry_id_fkey FOREIGN KEY (entry_id) REFERENCES entries(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 1804 (class 2606 OID 16469)
-- Dependencies: 1508 1797 1511
-- Name: entries__tags_tag_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY entries__tags
    ADD CONSTRAINT entries__tags_tag_id_fkey FOREIGN KEY (tag_id) REFERENCES tags(id) ON UPDATE CASCADE ON DELETE CASCADE;


-- Completed on 2011-08-26 14:46:49

--
-- PostgreSQL database dump complete
--

