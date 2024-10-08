PGDMP  5    *                |            PontoComInformatica    16.3    16.3     �           0    0    ENCODING    ENCODING     !   SET client_encoding = 'WIN1252';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16404    PontoComInformatica    DATABASE     �   CREATE DATABASE "PontoComInformatica" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Portuguese_Brazil.1252';
 %   DROP DATABASE "PontoComInformatica";
                postgres    false            �            1259    16406    contas_a_pagar    TABLE     �   CREATE TABLE public.contas_a_pagar (
    id integer NOT NULL,
    descricao character varying(255) NOT NULL,
    valor numeric(10,2) NOT NULL,
    data_vencimento date NOT NULL,
    observacoes text
);
 "   DROP TABLE public.contas_a_pagar;
       public         heap    postgres    false            �            1259    16405    contas_a_pagar_id_seq    SEQUENCE     �   CREATE SEQUENCE public.contas_a_pagar_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.contas_a_pagar_id_seq;
       public          postgres    false    216            �           0    0    contas_a_pagar_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public.contas_a_pagar_id_seq OWNED BY public.contas_a_pagar.id;
          public          postgres    false    215            �            1259    16413    contas_a_receber    TABLE     �   CREATE TABLE public.contas_a_receber (
    id integer NOT NULL,
    descricao character varying(255) NOT NULL,
    valor numeric(10,2) NOT NULL,
    data_recebimento date NOT NULL,
    observacoes text
);
 $   DROP TABLE public.contas_a_receber;
       public         heap    postgres    false            �            1259    16412    contas_a_receber_id_seq    SEQUENCE     �   CREATE SEQUENCE public.contas_a_receber_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.contas_a_receber_id_seq;
       public          postgres    false    218            �           0    0    contas_a_receber_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.contas_a_receber_id_seq OWNED BY public.contas_a_receber.id;
          public          postgres    false    217                       2604    16409    contas_a_pagar id    DEFAULT     v   ALTER TABLE ONLY public.contas_a_pagar ALTER COLUMN id SET DEFAULT nextval('public.contas_a_pagar_id_seq'::regclass);
 @   ALTER TABLE public.contas_a_pagar ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    215    216    216                        2604    16416    contas_a_receber id    DEFAULT     z   ALTER TABLE ONLY public.contas_a_receber ALTER COLUMN id SET DEFAULT nextval('public.contas_a_receber_id_seq'::regclass);
 B   ALTER TABLE public.contas_a_receber ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    218    217    218            �          0    16406    contas_a_pagar 
   TABLE DATA           \   COPY public.contas_a_pagar (id, descricao, valor, data_vencimento, observacoes) FROM stdin;
    public          postgres    false    216   �       �          0    16413    contas_a_receber 
   TABLE DATA           _   COPY public.contas_a_receber (id, descricao, valor, data_recebimento, observacoes) FROM stdin;
    public          postgres    false    218          �           0    0    contas_a_pagar_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.contas_a_pagar_id_seq', 1, true);
          public          postgres    false    215            �           0    0    contas_a_receber_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.contas_a_receber_id_seq', 3, true);
          public          postgres    false    217            "           2606    16411 "   contas_a_pagar contas_a_pagar_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.contas_a_pagar
    ADD CONSTRAINT contas_a_pagar_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY public.contas_a_pagar DROP CONSTRAINT contas_a_pagar_pkey;
       public            postgres    false    216            $           2606    16418 &   contas_a_receber contas_a_receber_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.contas_a_receber
    ADD CONSTRAINT contas_a_receber_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.contas_a_receber DROP CONSTRAINT contas_a_receber_pkey;
       public            postgres    false    218            �      x������ � �      �      x������ � �     