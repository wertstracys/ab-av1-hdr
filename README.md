---
### 🌟 PsyEncoder
---
```
FROM encodev/svtav1enc:hdr
WORKDIR /usr/src/app
RUN chmod -R 777 /usr
COPY .env .
CMD ["bash", "run.sh"]
```
