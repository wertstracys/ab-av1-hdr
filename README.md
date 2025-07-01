---
### 🌟 PsyEncoder
---
```
FROM encodev/svtav1enc:hdr
WORKDIR /bot
RUN chmod -R 777 /bot
COPY .env .
CMD ["bash", "run.sh"]
```
