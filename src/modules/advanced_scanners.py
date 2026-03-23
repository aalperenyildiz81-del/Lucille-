"""
Example scanner modules for Lucille
These are advanced implementations combining features from Sn1per, Nikto, and Recon-ng
"""

import socket
import dns.resolver
import dns.zone
import requests
from typing import Dict, List, Any
from .._core.module_manager import LucilleModule


class AdvancedPortScanModule(LucilleModule):
    """Advanced port scanning with service discovery"""
    
    name = "port_scan"
    description = "Advanced network port scanning with service fingerprinting"
    category = "reconnaissance"
    
    COMMON_PORTS = {
        22: 'ssh',
        25: 'smtp',
        53: 'dns',
        80: 'http',
        110: 'pop3',
        143: 'imap',
        443: 'https',
        445: 'smb',
        3306: 'mysql',
        3389: 'rdp',
        5432: 'postgres',
        5984: 'couchdb',
        6379: 'redis',
        8080: 'http-proxy',
        8443: 'https-proxy',
        9000: 'http-alt',
        27017: 'mongodb'
    }
    
    def execute(self, target: str, timeout: int = 30) -> Dict[str, Any]:
        """Scan ports and identify services"""
        results = {
            'target': target,
            'open_ports': [],
            'services': {},
            'banners': {},
            'vulnerabilities': []
        }
        
        # Scan common ports
        for port, service in self.COMMON_PORTS.items():
            if self._port_open(target, port, timeout):
                results['open_ports'].append(port)
                results['services'][str(port)] = service
                
                # Try to grab banner
                banner = self._grab_banner(target, port)
                if banner:
                    results['banners'][str(port)] = banner
        
        return results
    
    def _port_open(self, host: str, port: int, timeout: int) -> bool:
        """Check if port is open"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout / len(self.COMMON_PORTS))
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def _grab_banner(self, host: str, port: int) -> str:
        """Try to grab service banner"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((host, port))
            data = sock.recv(1024).decode('utf-8', errors='ignore')
            sock.close()
            return data.strip()
        except:
            return None


class DNSEnumerationModule(LucilleModule):
    """Advanced DNS reconnaissance module"""
    
    name = "dns_recon"
    description = "Comprehensive DNS enumeration and reconnaissance"
    category = "reconnaissance"
    
    def execute(self, target: str, timeout: int = 30) -> Dict[str, Any]:
        """Perform DNS reconnaissance"""
        results = {
            'target': target,
            'a_records': [],
            'aaaa_records': [],
            'mx_records': [],
            'cname_records': [],
            'txt_records': [],
            'ns_records': [],
            'soa_records': [],
            'issues': []
        }
        
        try:
            # Query A records
            results['a_records'] = self._query_dns(target, 'A')
        except:
            results['issues'].append('Could not query A records')
        
        try:
            # Query AAAA records
            results['aaaa_records'] = self._query_dns(target, 'AAAA')
        except:
            pass
        
        try:
            # Query MX records
            results['mx_records'] = [str(rdata) for rdata in self._query_dns(target, 'MX')]
        except:
            results['issues'].append('Could not query MX records')
        
        try:
            # Query NS records
            results['ns_records'] = [str(rdata) for rdata in self._query_dns(target, 'NS')]
        except:
            results['issues'].append('Could not query NS records')
        
        try:
            # Query TXT records
            results['txt_records'] = [str(rdata) for rdata in self._query_dns(target, 'TXT')]
        except:
            pass
        
        # Check for zone transfer vulnerability
        if self._check_zone_transfer(target):
            results['issues'].append('CRITICAL: Zone transfer possible!')
        
        return results
    
    def _query_dns(self, target: str, record_type: str) -> List:
        """Query DNS records"""
        try:
            answers = dns.resolver.query(target, record_type)
            return [str(rdata) for rdata in answers]
        except:
            return []
    
    def _check_zone_transfer(self, target: str) -> bool:
        """Check for zone transfer vulnerability"""
        try:
            zone = dns.zone.from_xfr(dns.query.xfr(target, target))
            return True
        except:
            return False


class WebVulnerabilityScanModule(LucilleModule):
    """Advanced web vulnerability scanning (Nikto-inspired)"""
    
    name = "web_vulnerability_scan"
    description = "Advanced HTTP/HTTPS vulnerability scanning"
    category = "vulnerability_scan"
    
    VULNERABLE_PATHS = [
        '/admin', '/admin.php', '/administrator',
        '/config.php', '/config.xml',
        '/.env', '/.git', '/.aws',
        '/backup', '/backups',
        '/test', '/debug',
        '/wp-admin', '/wp-login.php',
        '/wp-content', '/wp-includes'
    ]
    
    def execute(self, target: str, timeout: int = 30) -> Dict[str, Any]:
        """Perform web vulnerability scan"""
        results = {
            'target': target,
            'status_code': None,
            'headers': {},
            'vulnerabilities': [],
            'technologies': [],
            'issues': []
        }
        
        # Normalize target URL
        if not target.startswith(('http://', 'https://')):
            target_url = f"http://{target}"
        else:
            target_url = target
        
        try:
            # Get basic information
            response = requests.get(target_url, timeout=timeout, allow_redirects=True)
            results['status_code'] = response.status_code
            results['headers'] = dict(response.headers)
            
            # Check for missing security headers
            security_headers = [
                'X-Frame-Options',
                'X-Content-Type-Options',
                'Content-Security-Policy',
                'Strict-Transport-Security'
            ]
            
            for header in security_headers:
                if header not in response.headers:
                    results['issues'].append(f"Missing security header: {header}")
            
            # Check for vulnerable paths
            for path in self.VULNERABLE_PATHS:
                check_url = target_url + path
                try:
                    path_response = requests.head(check_url, timeout=2)
                    if path_response.status_code < 400:
                        results['vulnerabilities'].append({
                            'type': 'Accessible Admin Path',
                            'path': path,
                            'status_code': path_response.status_code
                        })
                except:
                    pass
            
            # Detect technologies
            results['technologies'] = self._detect_technologies(response)
            
        except Exception as e:
            results['issues'].append(f"Connection error: {str(e)}")
        
        return results
    
    def _detect_technologies(self, response: requests.Response) -> List[str]:
        """Detect web technologies"""
        technologies = []
        
        server = response.headers.get('Server', '')
        if server:
            technologies.append(server)
        
        x_powered_by = response.headers.get('X-Powered-By', '')
        if x_powered_by:
            technologies.append(x_powered_by)
        
        # Check for common signatures
        content = response.text.lower()
        if 'wordpress' in content:
            technologies.append('WordPress')
        if 'drupal' in content:
            technologies.append('Drupal')
        if 'joomla' in content:
            technologies.append('Joomla')
        
        return list(set(technologies))


class SubdomainEnumerationModule(LucilleModule):
    """Subdomain enumeration module"""
    
    name = "subdomain_enum"
    description = "Comprehensive subdomain discovery and enumeration"
    category = "reconnaissance"
    
    COMMON_SUBDOMAINS = [
        'www', 'mail', 'api', 'admin', 'staging', 'dev',
        'test', 'demo', 'beta', 'cdn', 'img', 'images',
        'assets', 'static', 'blog', 'shop', 'store',
        'ftp', 'smtp', 'pop', 'imap', 'vpn',
        'ns1', 'ns2', 'dns', 'mail1', 'mail2'
    ]
    
    def execute(self, target: str, timeout: int = 30) -> Dict[str, Any]:
        """Enumerate subdomains"""
        results = {
            'target': target,
            'subdomains': [],
            'resolved': [],
            'unresolved': []
        }
        
        # Extract domain
        if '://' in target:
            target = target.split('://')[1].split('/')[0]
        
        # Remove www prefix
        domain = target.replace('www.', '')
        
        # Brute force common subdomains
        for subdomain in self.COMMON_SUBDOMAINS:
            full_domain = f"{subdomain}.{domain}"
            try:
                ip = socket.gethostbyname(full_domain)
                results['subdomains'].append(full_domain)
                results['resolved'].append({'subdomain': full_domain, 'ip': ip})
            except:
                results['unresolved'].append(full_domain)
        
        return results
