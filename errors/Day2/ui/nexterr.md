# previous npm install errors gone but now these

```bash
lsetga@lsetga:~/Projects/episteme/frontend$ npm run dev

> frontend@0.1.0 dev
> next dev

⚠ `images.domains` is deprecated in favor of `images.remotePatterns`. Please update next.config.ts to protect your application from malicious users.
⚠ Invalid next.config.ts options detected: 
⚠     Unrecognized key(s) in object: 'swcMinify'
⚠ See more info here: https://nextjs.org/docs/messages/invalid-next-config
▲ Next.js 16.1.6 (Turbopack)
- Local:         http://localhost:3000
- Network:       http://192.168.0.105:3000

✓ Starting...
✓ Ready in 16.9s
○ Compiling /demo ...
⨯ ./app/demo/page.tsx:3:1
Module not found: Can't resolve '@/lib/api'
  1 | 'use client';
  2 |
> 3 | import { api } from '@/lib/api';
    | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  4 | import { motion } from 'framer-motion';
  5 | import { useEffect, useState } from 'react';
  6 |

Import map: aliased to relative './lib/api' inside of [project]/


Import traces:
  Client Component Browser:
    ./app/demo/page.tsx [Client Component Browser]
    ./app/demo/page.tsx [Server Component]

  Client Component SSR:
    ./app/demo/page.tsx [Client Component SSR]
    ./app/demo/page.tsx [Server Component]

https://nextjs.org/docs/messages/module-not-found


 GET /demo 500 in 23.6s (compile: 22.2s, render: 1416ms)
 GET / 200 in 3.6s (compile: 2.4s, render: 1261ms)
⨯ ./app/demo/page.tsx:3:1
Module not found: Can't resolve '@/lib/api'
  1 | 'use client';
  2 |
> 3 | import { api } from '@/lib/api';
    | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  4 | import { motion } from 'framer-motion';
  5 | import { useEffect, useState } from 'react';
  6 |

Import map: aliased to relative './lib/api' inside of [project]/


Import traces:
  Client Component Browser:
    ./app/demo/page.tsx [Client Component Browser]
    ./app/demo/page.tsx [Server Component]

  Client Component SSR:
    ./app/demo/page.tsx [Client Component SSR]
    ./app/demo/page.tsx [Server Component]

https://nextjs.org/docs/messages/module-not-found


 GET /demo 500 in 796ms (compile: 381ms, render: 416ms)
 GET / 200 in 946ms (compile: 129ms, render: 817ms)
