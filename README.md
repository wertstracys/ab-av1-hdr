---
### 🌟 PsyEncoder
---
```
FROM encodev/svtav1enc:hdr

WORKDIR /bot
RUN chmod -R 777 /usr /bot

COPY .env .

CMD ["bash", "run.sh"]
```
