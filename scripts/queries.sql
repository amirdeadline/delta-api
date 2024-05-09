select * from "Tenant_1001"."network_app_vrf";
select * from "Tenant_1001"."network_app_transport";
INSERT INTO "Tenant_1001"."network_app_transport" (id, name, description,created_at, modified_at) 
VALUES 
(1, 'Internet', 'Internet Transport', '2023-07-13T08:27:56.253854', '2023-07-13T08:27:56.253865');

INSERT INTO "Tenant_1001"."interfacetypes" (type) 
VALUES 
('ethernet'),
('bonding'),
('dummy'),
('bridge'),
('openvpn'),
('loopback'),
('tunnel'),
('virtual-ethernet'),
('vti'),
('vxlan'),
('wireless'),
('wireguard'),
('wwan'),
('sstpc');

INSERT INTO "Tenant_1001"."interfaceroles" (role) 
VALUES 
('lan'),
('internet'),
('private_underlay'),
('v-internet'),
('v-ctrl'),
('sdwan'),
('sase'),
('mgmt'),
('ha'),
('ctrl');

INSERT INTO "Tenant_1001"."lacphashoptions"  (name) 
VALUES 
('layer2'),
('layer2+3'),
('layer3+4'),
('encap2+3'),
('encap3+4');

INSERT INTO "Tenant_1001"."edge_gateway_types" (type)
VALUES
('sg'),
('tg'),
('rag');


INSERT INTO "Tenant_1001"."base_devicemodels" (name)
VALUES
('virtual'),
('1100'),
('1200');

INSERT INTO "Tenant_1001"."base_softwareversions" (version)
VALUES
('1.0.0'),
('1.1.0'),
('1.1.1');

INSERT INTO "Tenant_1001"."vrfroles" (role)
VALUES
('ctrl'),
('lan'),
('underlay'),
('mgmt');

select * from "Tenant_1001"."network_app_vrf";

INSERT INTO "Tenant_1001"."network_app_vrf" (name, vrf_id ,role_id, created_at, modified_at) 
VALUES 
('ctrl', 100, 'ctrl', '2023-07-13T08:27:56.253854', '2023-07-13T08:27:56.253865'),
('mgmt', 199, 'mgmt', '2023-07-13T08:27:56.253854', '2023-07-13T08:27:56.253865'),
('lan', 200, 'lan', '2023-07-13T08:27:56.253854', '2023-07-13T08:27:56.253865'),
('inet1', 101, 'underlay', '2023-07-13T08:27:56.253854', '2023-07-13T08:27:56.253865'),
('inet2', 102, 'underlay', '2023-07-13T08:27:56.253854', '2023-07-13T08:27:56.253865');


INSERT INTO "Tenant_1001"."encryption" (name, description)
VALUES
    ('null', 'No encryption'),
    ('aes128', 'AES 128-bit encryption'),
    ('aes192', 'AES 192-bit encryption'),
    ('aes256', 'AES 256-bit encryption'),
    ('aes128ctr', 'AES 128-bit counter mode encryption'),
    ('aes192ctr', 'AES 192-bit counter mode encryption'),
    ('aes256ctr', 'AES 256-bit counter mode encryption'),
    ('aes128ccm64', 'AES 128-bit CCM encryption with 64-bit tag'),
    ('aes192ccm64', 'AES 192-bit CCM encryption with 64-bit tag'),
    ('aes256ccm64', 'AES 256-bit CCM encryption with 64-bit tag'),
    ('aes128ccm96', 'AES 128-bit CCM encryption with 96-bit tag'),
    ('aes192ccm96', 'AES 192-bit CCM encryption with 96-bit tag'),
    ('aes256ccm96', 'AES 256-bit CCM encryption with 96-bit tag'),
    ('aes128ccm128', 'AES 128-bit CCM encryption with 128-bit tag'),
    ('aes192ccm128', 'AES 192-bit CCM encryption with 128-bit tag'),
    ('aes256ccm128', 'AES 256-bit CCM encryption with 128-bit tag'),
    ('aes128gcm64', 'AES 128-bit GCM encryption with 64-bit tag'),
    ('aes192gcm64', 'AES 192-bit GCM encryption with 64-bit tag'),
    ('aes256gcm64', 'AES 256-bit GCM encryption with 64-bit tag'),
    ('aes128gcm96', 'AES 128-bit GCM encryption with 96-bit tag'),
    ('aes192gcm96', 'AES 192-bit GCM encryption with 96-bit tag'),
    ('aes256gcm96', 'AES 256-bit GCM encryption with 96-bit tag'),
    ('aes128gcm128', 'AES 128-bit GCM encryption with 128-bit tag'),
    ('aes192gcm128', 'AES 192-bit GCM encryption with 128-bit tag'),
    ('aes256gcm128', 'AES 256-bit GCM encryption with 128-bit tag'),
    ('aes128gmac', 'AES 128-bit GMAC encryption'),
    ('aes192gmac', 'AES 192-bit GMAC encryption'),
    ('aes256gmac', 'AES 256-bit GMAC encryption'),
    ('3des', 'Triple DES encryption'),
    ('blowfish128', 'Blowfish 128-bit encryption'),
    ('blowfish192', 'Blowfish 192-bit encryption'),
    ('blowfish256', 'Blowfish 256-bit encryption'),
    ('camellia128', 'Camellia 128-bit encryption'),
    ('camellia192', 'Camellia 192-bit encryption'),
    ('camellia256', 'Camellia 256-bit encryption'),
    ('camellia128ctr', 'Camellia 128-bit counter mode encryption'),
    ('camellia192ctr', 'Camellia 192-bit counter mode encryption'),
    ('camellia256ctr', 'Camellia 256-bit counter mode encryption'),
    ('camellia128ccm64', 'Camellia 128-bit CCM encryption with 64-bit tag'),
    ('camellia192ccm64', 'Camellia 192-bit CCM encryption with 64-bit tag'),
    ('camellia256ccm64', 'Camellia 256-bit CCM encryption with 64-bit tag'),
    ('camellia128ccm96', 'Camellia 128-bit CCM encryption with 96-bit tag'),
    ('camellia192ccm96', 'Camellia 192-bit CCM encryption with 96-bit tag'),
    ('camellia256ccm96', 'Camellia 256-bit CCM encryption with 96-bit tag'),
    ('camellia128ccm128', 'Camellia 128-bit CCM encryption with 128-bit tag'),
    ('camellia192ccm128', 'Camellia 192-bit CCM encryption with 128-bit tag'),
    ('camellia256ccm128', 'Camellia 256-bit CCM encryption with 128-bit tag'),
    ('serpent128', 'Serpent 128-bit encryption'),
    ('serpent192', 'Serpent 192-bit encryption'),
    ('serpent256', 'Serpent 256-bit encryption'),
    ('twofish128', 'Twofish 128-bit encryption'),
    ('twofish192', 'Twofish 192-bit encryption'),
    ('twofish256', 'Twofish 256-bit encryption'),
    ('cast128', 'CAST 128-bit encryption'),
    ('chacha20poly1305', 'ChaCha20-Poly1305 encryption');
   
  

INSERT INTO "Tenant_1001"."hash" (name, description)
VALUES
    ('md5', 'MD5 hash algorithm'),
    ('md5_128', 'MD5 hash algorithm with 128-bit output'),
    ('sha1', 'SHA-1 hash algorithm'),
    ('sha1_160', 'SHA-1 hash algorithm with 160-bit output'),
    ('sha256', 'SHA-256 hash algorithm'),
    ('sha256_96', 'SHA-256 hash algorithm with 96-bit output'),
    ('sha384', 'SHA-384 hash algorithm'),
    ('sha512', 'SHA-512 hash algorithm'),
    ('aesxcbc', 'AES-XCBC hash algorithm'),
    ('aescmac', 'AES-CMAC hash algorithm'),
    ('aes128gmac', 'AES 128-bit GMAC hash algorithm'),
    ('aes192gmac', 'AES 192-bit GMAC hash algorithm'),
    ('aes256gmac', 'AES 256-bit GMAC hash algorithm');

INSERT INTO "Tenant_1001"."dhgroup" ("group", description)
VALUES
    (1, 'Diffie-Hellman Group 1'),
    (2, 'Diffie-Hellman Group 2'),
    (5, 'Diffie-Hellman Group 5'),
    (14, 'Diffie-Hellman Group 14'),
    (15, 'Diffie-Hellman Group 15'),
    (16, 'Diffie-Hellman Group 16'),
    (17, 'Diffie-Hellman Group 17'),
    (18, 'Diffie-Hellman Group 18'),
    (19, 'Diffie-Hellman Group 19'),
    (20, 'Diffie-Hellman Group 20'),
    (21, 'Diffie-Hellman Group 21'),
    (22, 'Diffie-Hellman Group 22'),
    (23, 'Diffie-Hellman Group 23'),
    (24, 'Diffie-Hellman Group 24'),
    (25, 'Diffie-Hellman Group 25'),
    (26, 'Diffie-Hellman Group 26'),
    (27, 'Diffie-Hellman Group 27'),
    (28, 'Diffie-Hellman Group 28'),
    (29, 'Diffie-Hellman Group 29'),
    (30, 'Diffie-Hellman Group 30'),
    (31, 'Diffie-Hellman Group 31'),
    (32, 'Diffie-Hellman Group 32');
    
 
DO $$
DECLARE 
  ip text := '169.254.1.0';
  last inet := '169.254.253.255';
  parts text[];
  third_octet int;
  fourth_octet int;
BEGIN
  WHILE ip::inet <= last LOOP
    parts := string_to_array(ip, '.');
    third_octet := parts[3]::int;
    fourth_octet := parts[4]::int;
    
    IF fourth_octet % 2 = 0 THEN
      INSERT INTO "Tenant_1001"."available_ip" (address) VALUES (ip::inet);
    END IF;

    fourth_octet := fourth_octet + 1;

    IF fourth_octet > 255 THEN
      fourth_octet := 0;
      third_octet := third_octet + 1;
    END IF;

    parts[3] := third_octet::text;
    parts[4] := fourth_octet::text;

    ip := array_to_string(parts, '.');
  END LOOP;
END $$;


INSERT INTO "Tenant_1001".profiles_app_slaprofile 
(created_at, modified_at, name, delay, interval, period, jitter, timeout, success_count, threshold, mos, packetloss)
VALUES 
('2023-07-13T12:11:53.887518', '2023-07-13T12:11:53.887530', 'Default SLA profile', 150, 1000, 5, 30, 500, 100, 3, 4.5, 15.0);


INSERT INTO "Tenant_1001".profiles_app_underlayprofile 
(id, created_at, modified_at, name, transport_id, sla_profile_id, nat, shaping,control, priority,underlay_monitor  )
VALUES 
(1, '2023-07-13T12:11:53.887518', '2023-07-13T12:11:53.887530','Internet Default Underlay Profile', 1, 1, true, true, true, 100, true);

INSERT INTO "Tenant_1001".profiles_app_bfdprofile 
(id, created_at, modified_at, name, interval_receive, interval_transmit, multiplier, enabled)
VALUES 
(1, '2023-07-13T12:11:53.887518', '2023-07-13T12:11:53.887530','Default BFD Profile', 500, 500, 3, true);


INSERT INTO "Tenant_1001".profiles_app_ipsecprofile 
(id, created_at, modified_at, name, certificate_auth, dead_peer_detection, ike_lifetime, tunnel_mode)
VALUES 
(1, '2023-07-13T12:15:35.382102', '2023-07-13T12:15:35.382114', 'Default SNMP Profile', false, false, NULL, true);


 select * from "Tenant_1001"."available_ip";

 select * from "Tenant_1001"."sites_app_sdwanoverlay";