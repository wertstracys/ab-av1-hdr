---
### 🌟 PsyEncoder
---
```
FROM encodev/svtav1enc:hdr
WORKDIR /bot
COPY .env .
CMD ["bash", "run.sh"]
```
