// A self-contained room: fresh artwork, live typography, native dialog controls.
// Coordinates refer to assets/experience/world.jpg (1716 × 917).
const projects = [
  { title: 'Ramco Institute of Technology', file: 'pr5.png', category: 'Education website',
    detailTitle: 'Ramco Institute Of Technology - Official College Website',
    detailHtml: `
      <p>The official public web portal of <mark class="project-highlight project-highlight--gold">Ramco Institute of Technology (RIT)</mark>, Rajapalayam. Designed as a premium, highly responsive administrative and marketing site, it incorporates micro-interactions, three-dimensional animations, and smooth kinetic scrolling to reflect the institution's forward-thinking tech brand.</p>
      <p><strong>Key features and components include:</strong></p>
      <ul>
        <li><strong>Frontend Engine:</strong> Designed on <mark class="project-highlight project-highlight--green">React 19</mark> and Vite with Tailwind CSS, utilizing Framer Motion and GSAP for performance-optimized transition animations.</li>
        <li><strong>Creative Assets:</strong> Embedded particle systems (tsParticles) and WebGL-based visual nodes (React Three Fiber) to create interactive backdrop modules.</li>
        <li><strong>Backend Core:</strong> Scalable web APIs implemented with Django and Django REST Framework.</li>
        <li><strong>Database:</strong> Secure storage handling academic departments, facilities, and staff rosters with SQLite and PostgreSQL.</li>
        <li><strong>Developer Workflows:</strong> Standardized with ESLint rules, styled component layers, and package scripts.</li>
      </ul>
      <h4>Technologies</h4>
      <ul class="project-technologies">
        <li>HTML</li>
        <li>CSS</li>
        <li>TypeScript</li>
        <li>React 19</li>
        <li>Vite</li>
        <li>Tailwind CSS</li>
        <li>Framer Motion</li>
        <li>GSAP</li>
        <li>Lenis</li>
        <li>React Three Fiber (Three.js)</li>
        <li>tsParticles</li>
        <li>Chart.js</li>
        <li>React Router</li>
        <li>Radix UI</li>
        <li>Django</li>
        <li>Django REST Framework</li>
        <li>Python</li>
        <li>SQLite</li>
        <li>PostgreSQL</li>
      </ul>`
  },
  { title: 'InternLearn', file: 'pr3.png', category: 'AI learning platform',
    detailHtml: `
      <p>An <mark class="project-highlight project-highlight--gold">AI-powered academic learning</mark> and internship coordination platform. It serves as a unified workspace where students can enroll in curriculum courses, track internship milestones, and attend virtual code-review meetings directly through third-party conference endpoints.</p>
      <p><strong>Functional features:</strong></p>
      <ul>
        <li><strong>Client Application:</strong> Reusable modular views configured with React.js, Vite, and CSS layouts.</li>
        <li><strong>Server REST API:</strong> Core services configured using <mark class="project-highlight project-highlight--green">Python, Django</mark>, and Django REST Framework.</li>
        <li><strong>Storage layer:</strong> Relational entity mapping utilizing PostgreSQL database.</li>
        <li><strong>Scheduling &amp; Meetings:</strong> Integrated <mark class="project-highlight project-highlight--purple">Google Calendar API</mark> and Google Meet integration for automated event scheduling and room assignments.</li>
        <li><strong>Authentications:</strong> Stateless JSON Web Tokens (JWT) validating student credentials.</li>
        <li><strong>Production Deployment:</strong> Client pages served on Vercel with REST services hosted on Render.</li>
      </ul>
      <h4>Project Access</h4>
      <a class="project-demo" href="https://intern-learn-osvkzqlzn-jeyastephen025-1500s-projects.vercel.app/" target="_blank" rel="noopener noreferrer">Live Demo <span aria-hidden="true">↗</span></a>
      <h4>Technologies</h4>
      <ul class="project-technologies">
        <li>React.js</li>
        <li>Vite</li>
        <li>CSS</li>
        <li>JavaScript</li>
        <li>Django</li>
        <li>Django REST Framework</li>
        <li>Python</li>
        <li>PostgreSQL</li>
        <li>JWT</li>
        <li>Google Calendar API</li>
        <li>Google Meet Integration</li>
      </ul>`
  },
  { title: 'Postly', file: 'postly_img.png', category: 'Social media automation',
    detailHtml: `
      <p>A <mark class="project-highlight project-highlight--gold">self-hosted social media automation platform</mark> that converts a single content idea and media file into platform-ready posts for <mark class="project-highlight project-highlight--green">Instagram, Facebook, LinkedIn, and YouTube</mark>. One upload is expanded into per-network captions, hashtags, and formats, then queued for scheduled publishing from infrastructure the owner fully controls.</p>
      <p><strong>Platform architecture:</strong></p>
      <ul>
        <li><strong>Frontend:</strong> React 18 and Vite 5 on a custom CSS design system, delivering a responsive dashboard with live post previews and a scheduling queue.</li>
        <li><strong>AI:</strong> <mark class="project-highlight project-highlight--purple">Gemini 2.5 Flash</mark> with an Ollama vision fallback for media-aware caption and hashtag generation.</li>
        <li><strong>Publishing:</strong> Native platform APIs covering Instagram Reels, LinkedIn video, Facebook media, and YouTube uploads.</li>
        <li><strong>Backend:</strong> Node.js and Express handling <mark class="project-highlight project-highlight--gold">OAuth 2.0</mark>, token refresh, CSRF protection, and automated account discovery.</li>
        <li><strong>Security:</strong> SQLite storage with AES-256-GCM encrypted tokens, scrypt password hashing, and secure HTTP-only sessions.</li>
        <li><strong>Testing:</strong> Custom test harness spanning 23 suites and roughly 1,470 assertions covering OAuth and API failure scenarios.</li>
        <li><strong>Developer Tools:</strong> MCP server exposing live connection state to AI agents.</li>
      </ul>`
  },
  { title: 'Creative Developer Portfolio', file: 'Creative Developer Portfolio.png', category: 'Personal portfolio',
    detailTitle: 'Interactive Personal Portfolio Website',
    detailHtml: `
      <p>A <mark class="project-highlight project-highlight--gold">modern personal portfolio website</mark> designed to showcase my projects, technical skills, professional experience, achievements, and resume through an engaging, responsive interface. The application combines animated sections, interactive visual effects, and dedicated project pages to help visitors explore my work, understand my expertise, and connect with me.</p>
      <p><strong>Platform architecture:</strong></p>
      <ul>
        <li><strong>Frontend:</strong> <mark class="project-highlight project-highlight--green">React 19 and Next.js 16</mark> with TypeScript, delivering a component-based interface with dedicated pages for projects, skills, experience, achievements, resume, and contact information.</li>
        <li><strong>Styling &amp; Design:</strong> Tailwind CSS provides responsive layouts, reusable styles, and consistent typography across desktop and mobile devices.</li>
        <li><strong>Animations &amp; Interactions:</strong> Framer Motion, GSAP, and Lenis support animated transitions, scroll-driven effects, and smooth navigation.</li>
        <li><strong>3D &amp; Visual Effects:</strong> <mark class="project-highlight project-highlight--purple">Three.js, React Three Fiber, and Spline</mark> support interactive graphics and immersive visual components.</li>
        <li><strong>Project Showcase:</strong> Dedicated project detail pages present descriptions, technology stacks, features, and supporting information.</li>
        <li><strong>Content Management:</strong> A centralized TypeScript data file organizes personal information, projects, skills, experience, and achievements for straightforward updates.</li>
        <li><strong>User Experience:</strong> Light and dark themes, multilingual infrastructure using next-intl, interactive navigation, and responsive content sections.</li>
        <li><strong>Performance:</strong> Next.js image optimization with WebP and AVIF support, alongside dynamic loading for selected visual components.</li>
        <li><strong>Deployment:</strong> A single Next.js application that supports local development and production builds.</li>
      </ul>
      <h4>Technologies</h4>
      <ul class="project-technologies">
        <li>Next.js 16</li>
        <li>React 19</li>
        <li>TypeScript</li>
        <li>Tailwind CSS</li>
        <li>Framer Motion</li>
        <li>GSAP</li>
        <li>Lenis</li>
        <li>Three.js</li>
        <li>React Three Fiber</li>
        <li>Spline</li>
        <li>next-intl</li>
        <li>next-themes</li>
        <li>HTML5 / CSS3</li>
      </ul>`
  },
  { title: 'Intern Diaries', file: 'pr1.png', category: 'Internship management',
    detailHtml: `
      <p>A collaborative workflow management platform and team workspace designed to track software development lifecycles. Users can organize tasks, assign project issues, track progress with <mark class="project-highlight project-highlight--gold">visual boards</mark>, and manage internal documentation in a unified shared dashboard.</p>
      <p><strong>Project details:</strong></p>
      <ul>
        <li><strong>Dashboard view:</strong> Dynamic task boards showcasing statuses, deadlines, and responsible developers.</li>
        <li><strong>Technical execution:</strong> Designed with modular front-end templates connected to a <mark class="project-highlight project-highlight--green">Python microservice API</mark> for tracking active ticket assignments.</li>
        <li><strong>Workspaces:</strong> Flexible <mark class="project-highlight project-highlight--purple">sub-teams configuration</mark> supporting nested projects and private workspaces.</li>
      </ul>`
  },
  { title: 'Automatic Certificate Generator', file: 'pr2.png', category: 'Certificate generator',
    detailHtml: `
      <p>An <mark class="project-highlight project-highlight--gold">automated batch certificate generator</mark> and mailing tool designed to process event participation records. The platform allows coordinators to upload a CSV file containing participant names, compile <mark class="project-highlight project-highlight--green">custom PDF certificates</mark>, and email them to participants automatically in a single batch operation.</p>
      <p><strong>Component breakdown:</strong></p>
      <ul>
        <li><strong>Client interface:</strong> Single-page application built on <mark class="project-highlight project-highlight--purple">React.js</mark> and CSS styling.</li>
        <li><strong>Server back-end:</strong> Batch-processing microservice API configured with <mark class="project-highlight project-highlight--gold">Node.js and Express.js</mark>.</li>
        <li><strong>Rendering &amp; PDF:</strong> Custom vector shapes mapped on Canvas to compile templates into downloadable PDFs via PDFKit.</li>
        <li><strong>Parser engine:</strong> File streams handled with Multer to feed row data to CSV Parser.</li>
        <li><strong>Mail integration:</strong> Batch email dispatcher running on Nodemailer and Brevo SMTP relay servers.</li>
        <li><strong>Hosting:</strong> Node API deployed on Render with front-end pages served on Vercel.</li>
      </ul>`
  },
  { title: 'AI Object Detection System', file: 'object detection.png', category: 'Computer vision',
    detailHtml: `
      <p>An <mark class="project-highlight project-highlight--gold">AI-powered object detection system</mark> that analyzes images and live camera feeds to identify and locate multiple objects in real time using computer vision and deep learning. The application processes visual input through an object detection model, draws bounding boxes around detected objects, and displays their <mark class="project-highlight project-highlight--green">class labels and confidence scores</mark> through an intuitive, modern interface designed for real-time monitoring and visual analysis.</p>
      <p><strong>Platform architecture:</strong></p>
      <ul>
        <li><strong>Frontend:</strong> React 18 and Vite, delivering a responsive interface with image upload, live webcam capture, detection results, and real-time bounding box visualization.</li>
        <li><strong>AI / Computer Vision:</strong> Python-based deep learning pipeline using <mark class="project-highlight project-highlight--purple">OpenCV</mark> for image and video processing, integrated with a trained object detection model for identifying objects.</li>
        <li><strong>Object Detection:</strong> Detects multiple objects within an image or video frame and predicts their class labels, bounding box coordinates, and confidence scores.</li>
        <li><strong>Backend:</strong> Python with FastAPI for handling image inputs, webcam streams, detection requests, model inference, and returning results to the frontend.</li>
        <li><strong>Image &amp; Video Processing:</strong> Frame capture, image resizing, preprocessing, color conversion, and real-time processing to prepare visual data for model inference.</li>
        <li><strong>Real-Time Detection:</strong> Supports live webcam analysis by continuously capturing frames, running object detection, and displaying results with bounding boxes and labels.</li>
        <li><strong>User Experience:</strong> Modern dashboard with image preview, live camera feed, detected object details, confidence scores, and clear visual feedback.</li>
        <li><strong>Deployment:</strong> Separate frontend and AI inference services that can be run locally or deployed to a cloud environment.</li>
      </ul>
      <h4>Project Access</h4>
      <p>Local development: Frontend and backend services can be accessed through their configured local URLs. The system supports both uploaded images and live webcam detection.</p>
      <h4>Technologies</h4>
      <ul class="project-technologies">
        <li>React 18</li>
        <li>Vite</li>
        <li>Python</li>
        <li>FastAPI</li>
        <li>OpenCV</li>
        <li>Deep Learning</li>
        <li>Computer Vision</li>
        <li>Object Detection Model</li>
        <li>NumPy</li>
        <li>REST API</li>
        <li>Webcam / Video Processing</li>
        <li>HTML5 / CSS3</li>
        <li>JavaScript</li>
      </ul>`
  },
  { title: 'CCTV Surveillance System', file: 'ppe detection.png', category: 'Computer vision',
    detailHtml: `
      <p>An <mark class="project-highlight project-highlight--gold">AI-powered CCTV surveillance system</mark> that analyzes live camera feeds and recorded video to detect objects, monitor activities, and identify potentially suspicious events in real time using computer vision and deep learning. The application processes video frames through an object detection model, tracks detected objects, and presents surveillance insights through an intuitive, modern dashboard designed for <mark class="project-highlight project-highlight--green">real-time security monitoring</mark> and situational awareness.</p>
      <p><strong>Platform architecture:</strong></p>
      <ul>
        <li><strong>Frontend:</strong> React 18 and Vite, delivering a responsive surveillance dashboard with live camera feeds, video playback, detection results, and real-time monitoring controls.</li>
        <li><strong>AI / Computer Vision:</strong> Python-based deep learning pipeline using <mark class="project-highlight project-highlight--purple">OpenCV</mark> for video capture, frame processing, and visual analysis, integrated with an object detection model.</li>
        <li><strong>Object Detection:</strong> Detects and identifies multiple objects in CCTV footage, predicting their class labels, bounding box coordinates, and confidence scores.</li>
        <li><strong>Backend:</strong> Python with FastAPI for handling camera streams, video inputs, detection requests, model inference, and communication with the frontend through REST APIs and real-time streaming.</li>
        <li><strong>Video Processing:</strong> Captures and processes CCTV frames through resizing, preprocessing, color conversion, and frame-by-frame analysis for efficient model inference.</li>
        <li><strong>Real-Time Surveillance:</strong> Continuously analyzes live camera feeds, displays detected objects with bounding boxes and labels, and supports real-time monitoring of surveillance footage.</li>
        <li><strong>Monitoring &amp; Alerts:</strong> Presents detected object information, event details, and surveillance status through a centralized dashboard for easier observation and incident review.</li>
        <li><strong>User Experience:</strong> Modern dashboard with live video preview, camera management, detection overlays, event logs, confidence scores, and clear visual feedback.</li>
        <li><strong>Deployment:</strong> Separate frontend and AI inference services that can be run locally or deployed to a cloud or on-premises environment, depending on camera and infrastructure requirements.</li>
      </ul>
      <h4>Project Access</h4>
      <p>Local development: Frontend and backend services can be accessed through their configured local URLs. The system supports CCTV camera feeds, recorded video analysis, and real-time object detection through the surveillance dashboard.</p>
      <h4>Technologies</h4>
      <ul class="project-technologies">
        <li>React 18</li>
        <li>Vite</li>
        <li>Python</li>
        <li>FastAPI</li>
        <li>OpenCV</li>
        <li>Deep Learning</li>
        <li>Computer Vision</li>
        <li>Object Detection Model</li>
        <li>NumPy</li>
        <li>REST API</li>
        <li>CCTV / IP Camera Integration</li>
        <li>Real-Time Video Streaming</li>
        <li>Video Processing</li>
        <li>HTML5 / CSS3</li>
        <li>JavaScript</li>
      </ul>`
  },
  { title: 'Question Paper Generation', file: 'Question paper generation.png', category: 'Education tools',
    detailHtml: `
      <p>An <mark class="project-highlight project-highlight--gold">automated, in-house CBSE Question Paper Generator</mark> designed specifically for <strong class="project-school">Vinayaga Public School</strong>. This application streamlines the test creation process by utilizing <mark class="project-highlight project-highlight--green">AI models</mark> to intelligently draft, format, and generate complete CBSE-standard examination papers. By combining modern front-end design with robust text analysis and optical character recognition pipelines, it automates question bank ingestion and formats outputs directly into printable documents.</p>
      <p><strong>Key architectural pillars include:</strong></p>
      <ul>
        <li><strong>Frontend:</strong> Interactive web interfaces constructed using HTML, CSS, JavaScript, and Jinja2 templates.</li>
        <li><strong>Backend:</strong> Flask server implementation in Python coordinating application API requests.</li>
        <li><strong>Database layer:</strong> MySQL for structured relation storage alongside MongoDB for semi-structured question nodes.</li>
        <li><strong>AI/LLM integration:</strong> <mark class="project-highlight project-highlight--purple">Ollama (Llama 3)</mark> for contextual question generation and Sentence Transformers for semantic indexing/similarity mapping.</li>
        <li><strong>OCR &amp; Ingestion Pipeline:</strong> <code class="project-ocr">PaddleOCR</code>, pdf2image, and Poppler used to read, parse, and process existing printed syllabus resources or reference papers.</li>
        <li><strong>Document Engine:</strong> Automated output generation using python-docx and docx2pdf to export instantly editable Microsoft Word documents and ready-to-print PDFs.</li>
        <li><strong>Developer Environment:</strong> System version control and collaborative deployments powered by Git and GitHub.</li>
      </ul>`
  },
  { title: 'AI-Powered Screening Creation Platform', file: 'AI-Powered Resume Screening & Recruitment Portal.png', category: 'AI recruitment',
    detailHtml: `
      <p>A full-stack <mark class="project-highlight project-highlight--gold">AI-powered resume builder</mark> that helps users create professional, <mark class="project-highlight project-highlight--green">ATS-friendly resumes</mark> through structured profile inputs, customizable templates, and intelligent content assistance. Users can enter their education, experience, projects, skills, and achievements, then generate polished resume sections, preview the final document in real time, and export it for job applications.</p>
      <p><strong>Platform architecture:</strong></p>
      <ul>
        <li><strong>Frontend:</strong> React.js and Vite, delivering a responsive resume editor with live preview, section-based editing, template selection, and a modern dashboard.</li>
        <li><strong>AI:</strong> <mark class="project-highlight project-highlight--purple">Gemini API</mark> for generating and improving professional summaries, work experience descriptions, project descriptions, and skill-focused content.</li>
        <li><strong>Resume Builder:</strong> Dynamic form sections for personal details, education, experience, projects, certifications, achievements, and technical skills.</li>
        <li><strong>Templates:</strong> Customizable resume layouts with consistent typography, spacing, alignment, and responsive preview.</li>
        <li><strong>Backend:</strong> Node.js and Express handling authentication, user profiles, resume CRUD operations, AI requests, and export workflows.</li>
        <li><strong>Database:</strong> MongoDB for securely storing user accounts, resume data, selected templates, and saved versions.</li>
        <li><strong>Export:</strong> PDF resume generation with print-optimized layouts and downloadable, application-ready documents.</li>
        <li><strong>Security:</strong> JWT-based authentication, protected routes, input validation, and secure API handling.</li>
      </ul>
      <h4>Technologies</h4>
      <ul class="project-technologies">
        <li>React.js</li>
        <li>Vite</li>
        <li>Node.js</li>
        <li>Express.js</li>
        <li>MongoDB</li>
        <li>Gemini API</li>
        <li>JWT Authentication</li>
        <li>REST API</li>
        <li>HTML5 / CSS3</li>
        <li>PDF Generation</li>
      </ul>`
  },
  { title: 'Chrome Extension', file: 'pr8.png', category: 'Study assistant',
    detailHtml: `
      <p>An AI-powered learning assistant packaged as a Chrome browser extension built on Manifest V3. The extension processes current page contents and provides students with context-aware learning aids without forcing them to navigate away from their active study tab.</p>
      <p><strong>Core features &amp; components:</strong></p>
      <ul>
        <li><strong>Extension front-end:</strong> Light popup windows styled with HTML, CSS, and vanilla JavaScript.</li>
        <li><strong>Browser scripts:</strong> Content scripts executing safely inside page contexts to read the DOM and extract readable texts.</li>
        <li><strong>Cognitive layer:</strong> Connected directly to <mark class="project-highlight project-highlight--gold">Google Gemini API (Gemini 2.5 Flash)</mark> to generate summaries, contextual definitions, and quizzes.</li>
        <li><strong>Data management:</strong> Key preferences and study notes saved locally using the <mark class="project-highlight project-highlight--green">Chrome Storage API</mark>.</li>
        <li><strong>Productivity tools:</strong> One-click actions for page summarization, quiz card generation, and notes compiling.</li>
      </ul>`
  },

  { title: 'AI Voice-Controlled Healthcare Platform', file: 'Health Care Voice Agent.png', category: 'Healthcare voice assistant',
    detailHtml: `
      <p>An <mark class="project-highlight project-highlight--gold">AI-powered healthcare platform</mark> that enables users to find doctors, manage appointments, access medical records, review medications, and ask general health questions through <mark class="project-highlight project-highlight--green">natural voice conversations</mark>. The application converts speech into text, understands user requests using a locally running language model, performs validated healthcare actions, and responds with synthesized speech. A modern interface provides live transcripts, doctor cards, appointment details, and visual feedback while speech recognition, AI reasoning, and speech synthesis run locally.</p>
      <p><strong>Platform architecture:</strong></p>
      <ul>
        <li><strong>Frontend:</strong> React 18, TypeScript, and Vite, with Tailwind CSS and Framer Motion for a responsive healthcare dashboard and interactive voice interface.</li>
        <li><strong>AI / Language Understanding:</strong> <mark class="project-highlight project-highlight--purple">Ollama with Llama 3.2</mark> for interpreting requests, extracting relevant details, and supporting conversations that retain context across multiple turns.</li>
        <li><strong>Speech Recognition:</strong> faster-whisper converts spoken requests into text, supported by audio preprocessing and speech endpoint detection.</li>
        <li><strong>Voice Responses:</strong> Piper TTS generates spoken replies locally, allowing users to interact with the application through conversation.</li>
        <li><strong>Backend:</strong> Python with FastAPI for authentication, healthcare workflows, AI processing, REST APIs, and WebSocket communication.</li>
        <li><strong>Healthcare Management:</strong> Supports doctor discovery, availability checks, appointment booking, rescheduling and cancellation, medical record access, medication review, and health note capture.</li>
        <li><strong>Knowledge Retrieval:</strong> Retrieval-Augmented Generation (RAG) using local health information, nomic-embed-text embeddings, and pgvector to support general health questions.</li>
        <li><strong>Database:</strong> PostgreSQL with SQLAlchemy and Alembic for storing users, appointments, medical records, conversation state, and searchable knowledge.</li>
        <li><strong>Real-Time Communication:</strong> Browser microphone capture and WebSocket audio streaming, with spoken playback, live transcripts, and support for interrupting assistant responses.</li>
        <li><strong>Security &amp; Validation:</strong> JWT authentication, Argon2 password hashing, role-based access controls, resource ownership checks, and explicit confirmation before sensitive actions.</li>
        <li><strong>User Experience:</strong> Voice navigation, animated assistant states, appointment and doctor cards, and dedicated pages for records, medications, and conversations.</li>
        <li><strong>Deployment:</strong> Local development or Docker Compose deployment for the frontend, backend, and database, with Ollama running on the host machine.</li>
      </ul>
      <h4>Technologies</h4>
      <ul class="project-technologies">
        <li>React 18</li>
        <li>TypeScript</li>
        <li>Vite</li>
        <li>Tailwind CSS</li>
        <li>Framer Motion</li>
        <li>Zustand</li>
        <li>Python</li>
        <li>FastAPI</li>
        <li>Ollama / Llama 3.2</li>
        <li>faster-whisper</li>
        <li>Piper TTS</li>
        <li>PostgreSQL</li>
        <li>pgvector</li>
        <li>SQLAlchemy / Alembic</li>
        <li>Retrieval-Augmented Generation (RAG)</li>
        <li>nomic-embed-text</li>
        <li>NumPy / SciPy</li>
        <li>REST API / WebSockets</li>
        <li>Web Audio API</li>
        <li>JWT Authentication</li>
        <li>Docker Compose</li>
      </ul>`
  },
];
// Each project occupies a screen in the room.
const experiences = projects;

const section = document.getElementById('projects');
const screens = document.getElementById('experienceScreens');
const dialog = document.getElementById('experienceDetail');
const reduced = matchMedia('(prefers-reduced-motion: reduce)');

// Corners measured from the room reference, clockwise from top left.
const outlines = [
  [[627,49],[1055,53],[1050,276],[628,277]],
  [[296,55],[596,194],[573,358],[260,249]],
  [[1078,200],[1365,76],[1412,282],[1104,359]],
  [[132,242],[390,344],[368,488],[92,427]],
  [[445,360],[626,406],[617,527],[432,496]],
  [[642,410],[765,422],[762,536],[635,529]],
  [[784,424],[920,423],[920,539],[783,539]],
  [[938,421],[1070,410],[1077,532],[939,537]],
  [[1088,406],[1243,364],[1267,502],[1100,530]],
  [[1298,335],[1554,231],[1598,430],[1324,486]],
  [[161,490],[434,526],[435,678],[152,685]],
  [[1225,525],[1507,492],[1518,690],[1225,679]],
];
const layerImages = [];
const planes = [];
const preview = document.createElement('img');
preview.className = 'experience__preview';
preview.alt = '';
document.getElementById('experienceDetailTitle').after(preview);

// Map a rectangular HTML screen to its measured quadrilateral. Keeping the
// screenshot and its button on the same plane preserves pointer hit testing.
function projectMatrix(points, scale) {
  const [[x0,y0],[x1,y1],[x2,y2],[x3,y3]] = points.map(([x,y]) => [x*scale,y*scale]);
  const dx1=x1-x2, dx2=x3-x2, dx3=x0-x1+x2-x3;
  const dy1=y1-y2, dy2=y3-y2, dy3=y0-y1+y2-y3;
  const det=dx1*dy2-dx2*dy1;
  const g=(dx3*dy2-dx2*dy3)/det, h=(dx1*dy3-dx3*dy1)/det;
  return `matrix3d(${[(x1-x0+g*x1)/400,(y1-y0+g*y1)/400,0,g/400,(x3-x0+h*x3)/225,(y3-y0+h*y3)/225,0,h/225,0,0,1,0,x0,y0,0,1].join(',')})`;
}

for (const [index, project] of experiences.entries()) {
  const points = outlines[index];
  const x=Math.min(...points.map(p=>p[0])), y=Math.min(...points.map(p=>p[1]));
  const w=Math.max(...points.map(p=>p[0]))-x, h=Math.max(...points.map(p=>p[1]))-y;
  const layer=document.createElement('div');
  layer.className='experience__card-layer';
  layer.style.cssText=`left:${x/1716*100}%;top:${y/917*100}%;width:${w/1716*100}%;height:${h/917*100}%`;
  const button=document.createElement('button');
  button.type='button';
  button.className='experience__screen experience__screen--project';
  const focal = { 'pr1.png': '18% 40%', 'pr2.png': '50% 40%', 'pr3.png': '50% 40%', 'pr5.png': '68% 40%', 'pr8.png': '50% 25%', 'postly_img.png': '68% 35%' };
  button.style.setProperty('--project-focus', focal[project.file] || '50% 50%');
  button.style.setProperty('--screen-accent', index % 3 === 0 ? '185, 75, 51' : '198, 163, 116');
  if(index===0) button.classList.add('experience__screen--hero');
  button.setAttribute('aria-haspopup','dialog');
  button.setAttribute('aria-label', `View ${project.title} — ${project.category}`);
  const img=new Image();
  img.src=`public/projects/${project.file}`;
  img.alt='';
  img.draggable=false;
  img.className='experience__project-image';
  layerImages.push(img);
  const label=document.createElement('span');
  label.className='experience__project-label';
  label.textContent=project.title;
  const indexLabel=document.createElement('span');
  indexLabel.className='experience__project-index';
  indexLabel.textContent=String(index+1).padStart(2,'0');
  indexLabel.setAttribute('aria-hidden','true');
  const category=document.createElement('span');
  category.className='experience__project-category';
  category.textContent=project.category;
  const action=document.createElement('span');
  action.className='experience__project-action';
  action.textContent='View project ↗';
  button.append(img,indexLabel,category,label,action);
  button.addEventListener('click',()=>{
    document.getElementById('experienceDetailCategory').textContent=project.category;
    document.getElementById('experienceDetailTitle').textContent=project.detailTitle || project.title;
    const detailCopy = document.getElementById('experienceDetailCopy');
    // Rich details are authored locally in the project data above.
    dialog.classList.toggle('experience__detail--rich', Boolean(project.detailHtml));
    if (project.detailHtml) detailCopy.innerHTML = project.detailHtml;
    else detailCopy.textContent = project.copy;
    preview.src=img.src;
    preview.alt=`${project.title} project screenshot`;
    dialog.showModal();
  });
  const order=[0,1,2,4,5,6,7,8,3,9,10,11];
  layer.style.setProperty('--arrival',`${160+order.indexOf(index)*85}ms`);
  layer.style.setProperty('--entry-turn',`${index%2?-6:6}deg`);
  layer.append(button);
  screens.append(layer);
  planes.push({button,points:points.map(([px,py])=>[px-x,py-y])});
}
const roomWorld=section.querySelector('.experience__world');
function fitProjects() {
  const scale=roomWorld.offsetWidth/1716;
  for(const plane of planes) plane.button.style.setProperty('--project-transform',projectMatrix(plane.points,scale));
}
fitProjects();
new ResizeObserver(fitProjects).observe(roomWorld);

// Composite the existing luminance matte into an alpha channel. Older iOS
// browsers treat CSS image masks as alpha-only and expose the source's
// checkerboard because both source files are opaque RGB images.
const person = document.createElement('div');
person.className = 'experience__person';
person.style.cssText = `left:${738 / 1716 * 100}%;top:${503 / 917 * 100}%;width:${242 / 1716 * 100}%;height:${361 / 917 * 100}%`;
const personImage = new Image();
personImage.src = 'assets/experience/person-source.png';
personImage.alt = '';
personImage.draggable = false;
const personMask = new Image();
personMask.src = 'assets/experience/person-mask.png';
const personCanvas = document.createElement('canvas');
personCanvas.className = 'experience__person-image';
personCanvas.setAttribute('aria-hidden', 'true');
person.append(personCanvas);
const personReady = Promise.all([personImage.decode(), personMask.decode()]).then(() => {
  personCanvas.width = personImage.naturalWidth;
  personCanvas.height = personImage.naturalHeight;
  const context = personCanvas.getContext('2d', { willReadFrequently: true });
  if (!context) throw new Error('Figure compositing unavailable');
  context.drawImage(personMask, 0, 0, personCanvas.width, personCanvas.height);
  const matte = context.getImageData(0, 0, personCanvas.width, personCanvas.height);
  context.drawImage(personImage, 0, 0);
  const figure = context.getImageData(0, 0, personCanvas.width, personCanvas.height);
  for (let i = 0; i < figure.data.length; i += 4) {
    figure.data[i + 3] = Math.round(
      .2126 * matte.data[i] + .7152 * matte.data[i + 1] + .0722 * matte.data[i + 2]);
  }
  context.putImageData(figure, 0, 0);
});
// Attach a rejection handler immediately; the fallback artwork stays visible.
personReady.catch(() => {});
screens.after(person);

// Load the room before switching away from the intact fallback artwork.
const room = new Image();
room.src = 'assets/experience/room.jpg';
Promise.all([room.decode(), personReady, ...layerImages.map(img => img.decode())]).then(() => {
  section.querySelector('.experience__art').src = room.src;
  section.classList.add('is-layered');
}).catch(() => { /* Keep the intact artwork if a layer cannot load. */ });

// Clicking the backdrop dismisses the dialog; Escape and focus restoration
// use native dialog behaviour.
dialog.addEventListener('click', (event) => {
  if (event.target !== dialog) return;
  const r = dialog.getBoundingClientRect();
  if (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom) dialog.close();
});

if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(([entry]) => {
    if (entry.intersectionRatio >= .22) {
      section.classList.add('is-visible');
    } else if (!entry.isIntersecting) section.classList.remove('is-visible');
  }, { threshold: [0, .22] });
  observer.observe(section);
} else section.classList.add('is-visible');

// Small screens keep the reference arrangement in an accessible scrollable
// room, initially centred on the figure. Tab scrolls each focused screen in.
const viewport = section.querySelector('.experience__viewport');
const narrow = matchMedia('(max-width: 700px)');
function centreRoom() {
  if (narrow.matches) requestAnimationFrame(() => {
    viewport.scrollLeft = (viewport.scrollWidth - viewport.clientWidth) / 2;
  });
}
centreRoom();
narrow.addEventListener('change', centreRoom);
screens.addEventListener('focusin', (event) => {
  if (narrow.matches) event.target.scrollIntoView({ block: 'nearest', inline: 'center', behavior: reduced.matches ? 'instant' : 'smooth' });
});

// Move artwork and its screen controls as one plane so the labels stay
// attached to the pictured displays. The fixed edge captions supply depth.
const world = section.querySelector('.experience__world');
const finePointer = matchMedia('(hover: hover) and (pointer: fine)');
const motion = { x: 0, y: 0, tx: 0, ty: 0, presence: 0, targetPresence: 0, raf: 0, last: 0 };
let roomOnScreen = false;
const canTilt = () => finePointer.matches && !narrow.matches && !reduced.matches && !dialog.open;

function paintRoom(now = performance.now()) {
  const idle = (roomOnScreen && !reduced.matches && !dialog.open)
    ? (1 - motion.presence)
    : 0;
  const idleX = idle * Math.sin(now * 0.00075) * 0.28;
  const idleY = idle * Math.cos(now * 0.00055) * 0.20;
  const curX = motion.x + idleX;
  const curY = motion.y + idleY;

  world.style.setProperty('--room-x', `${(curX * 9).toFixed(3)}px`);
  world.style.setProperty('--room-y', `${(curY * 5).toFixed(3)}px`);
  world.style.setProperty('--room-rx', `${(-curY * 3).toFixed(3)}deg`);
  world.style.setProperty('--room-ry', `${(curX * 4).toFixed(3)}deg`);
  world.style.setProperty('--room-scale', (1 + Math.max(motion.presence, 0.25 * idle) * .035).toFixed(5));
  world.style.setProperty('--room-light-x', `${50 + curX * 35}%`);
  world.style.setProperty('--room-light-y', `${50 + curY * 35}%`);
  world.style.setProperty('--room-light', Math.max(motion.presence, 0.35 * idle).toFixed(4));
}

function animateRoom(now) {
  const dt = Math.min((now - motion.last) / 1000, .05);
  motion.last = now;
  const ease = 1 - Math.exp(-7 * dt);
  motion.x += (motion.tx - motion.x) * ease;
  motion.y += (motion.ty - motion.y) * ease;
  motion.presence += (motion.targetPresence - motion.presence) * ease;
  const settled = Math.abs(motion.tx - motion.x) + Math.abs(motion.ty - motion.y)
    + Math.abs(motion.targetPresence - motion.presence) < .001;
  if (settled) {
    motion.x = motion.tx;
    motion.y = motion.ty;
    motion.presence = motion.targetPresence;
  }
  paintRoom(now);
  const shouldLoop = (roomOnScreen && !reduced.matches && !dialog.open) || !settled;
  motion.raf = shouldLoop ? requestAnimationFrame(animateRoom) : 0;
  if (!shouldLoop && !motion.presence) section.classList.remove('is-tracking');
}

function wakeRoom() {
  if (motion.raf) return;
  motion.last = performance.now();
  section.classList.add('is-tracking');
  motion.raf = requestAnimationFrame(animateRoom);
}

function resetRoom(immediate = false) {
  motion.tx = motion.ty = motion.targetPresence = 0;
  if (immediate) {
    cancelAnimationFrame(motion.raf);
    motion.raf = 0;
    motion.x = motion.y = motion.presence = 0;
    paintRoom();
    section.classList.remove('is-tracking');
  } else wakeRoom();
}

section.addEventListener('pointermove', (event) => {
  if (!canTilt() || event.pointerType === 'touch') return;
  const r = viewport.getBoundingClientRect();
  motion.tx = Math.max(-1, Math.min(1, (event.clientX - r.left) / r.width * 2 - 1));
  motion.ty = Math.max(-1, Math.min(1, (event.clientY - r.top) / r.height * 2 - 1));
  motion.targetPresence = 1;
  wakeRoom();
}, { passive: true });
section.addEventListener('pointerleave', () => resetRoom(!canTilt()));
section.addEventListener('pointercancel', () => resetRoom(true));
screens.addEventListener('click', () => resetRoom(reduced.matches));
for (const query of [finePointer, narrow, reduced]) {
  query.addEventListener('change', () => resetRoom(true));
}
document.addEventListener('visibilitychange', () => {
  if (document.hidden) resetRoom(true);
});
if ('IntersectionObserver' in window) {
  new IntersectionObserver(([entry]) => {
    roomOnScreen = entry.isIntersecting;
    if (roomOnScreen) wakeRoom();
    else resetRoom(true);
  }).observe(section);
}
