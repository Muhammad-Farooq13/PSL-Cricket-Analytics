# Security Policy

## Reporting Security Vulnerabilities

If you discover a security vulnerability in this project, please email **mfarooqshafee333@gmail.com** instead of using the issue tracker.

Please include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

## Security Best Practices

When deploying this project:

1. **Never commit secrets** to version control
2. **Use environment variables** for sensitive data
3. **Keep dependencies updated** - Run `pip install --upgrade -r requirements.txt`
4. **Enable HTTPS** in production
5. **Use strong credentials** for database and API access
6. **Implement API authentication** for production deployments
7. **Monitor logs** for suspicious activity
8. **Configure firewall rules** properly
9. **Use secrets management** tools for production

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.0.x   | ✅ Yes    |

## Updates

We recommend keeping your dependencies updated. Check for updates regularly:

```bash
pip list --outdated
pip install --upgrade pip
pip install -r requirements.txt --upgrade
```
