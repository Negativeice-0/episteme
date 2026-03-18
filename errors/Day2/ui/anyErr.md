# If you went straight to browser you might see less errors

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
✓ Ready in 17.2s
○ Compiling / ...
 GET / 200 in 20.7s (compile: 19.4s, render: 1349ms)
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



./app/demo/page.tsx:4:1
Module not found: Can't resolve 'framer-motion'
  2 |
  3 | import { api } from '@/lib/api';
> 4 | import { motion } from 'framer-motion';
    | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  5 | import { useEffect, useState } from 'react';
  6 |
  7 | export default function DemoPage() {



Import traces:
  Client Component Browser:
    ./app/demo/page.tsx [Client Component Browser]
    ./app/demo/page.tsx [Server Component]

  Client Component SSR:
    ./app/demo/page.tsx [Client Component SSR]
    ./app/demo/page.tsx [Server Component]

https://nextjs.org/docs/messages/module-not-found


○ Compiling /_error ...
 GET /demo 500 in 22.2s (compile: 20.0s, render: 2.2s)
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



./app/demo/page.tsx:4:1
Module not found: Can't resolve 'framer-motion'
  2 |
  3 | import { api } from '@/lib/api';
> 4 | import { motion } from 'framer-motion';
    | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  5 | import { useEffect, useState } from 'react';
  6 |
  7 | export default function DemoPage() {



Import traces:
  Client Component Browser:
    ./app/demo/page.tsx [Client Component Browser]
    ./app/demo/page.tsx [Server Component]

  Client Component SSR:
    ./app/demo/page.tsx [Client Component SSR]
    ./app/demo/page.tsx [Server Component]

https://nextjs.org/docs/messages/module-not-found


 GET /demo 500 in 876ms (compile: 596ms, render: 281ms)
