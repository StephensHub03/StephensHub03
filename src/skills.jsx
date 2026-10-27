import React, { useEffect, useRef } from 'react';
import { createRoot } from 'react-dom/client';
import { siReact, siPython, siDjango, siNodedotjs, siPostgresql, siFirebase, siNextdotjs, siJavascript, siTailwindcss, siHtml5, siClaude, siN8n, siMake, siLangchain, siCursor, siGit, siGithub, siNotion, siDocker, siPostman } from 'simple-icons';
const icons = { siReact, siPython, siDjango, siNodedotjs, siPostgresql, siFirebase, siNextdotjs, siJavascript, siTailwindcss, siHtml5, siClaude, siN8n, siMake, siLangchain, siCursor, siGit, siGithub, siNotion, siDocker, siPostman };
import { Lightbulb, MessageSquare, Sparkles, Users, ChartNoAxesCombined } from 'lucide-react';

const skill = (name, slug, color, fallback) => ({ name, slug, color, fallback });
const categories = [
  ['Design & Creative', 'Ideas into experiences', [skill('Google Flow', null, '#bc70ff', 'Flow'), skill('Veo', null, '#a995ff', 'Veo'), skill('MotionSites', null, '#ae8ee8', 'MS'), skill('ReactBits', 'React', '#22c6e7'), skill('Higgsfield', null, '#dcff41', 'h')]],
  ['Backend', 'Build. Integrate. Scale.', [skill('Python', 'Python', '#ffd34b'), skill('Django', 'Django', '#e7f5ec'), skill('Node.js', 'Nodedotjs', '#75bd49'), skill('PostgreSQL', 'Postgresql', '#6599ca'), skill('Firebase', 'Firebase', '#ffae27')]],
  ['Frontend', 'Pixels to products', [skill('React', 'React', '#22c6e7'), skill('Next.js', 'Nextdotjs', '#fff'), skill('JavaScript', 'Javascript', '#f7df1e'), skill('Tailwind CSS', 'Tailwindcss', '#38bdf8'), skill('HTML5', 'Html5', '#f3532c'), skill('CSS3', null, '#4c70ff', 'CSS')]],
  ['AI & Automation', 'Think. Build. Automate.', [skill('OpenAI', 'Openai', '#fff', 'AI'), skill('Claude', 'Claude', '#d78660'), skill('n8n', 'N8n', '#ed596f'), skill('Make', 'Make', '#9862ff'), skill('LangChain', 'Langchain', '#72b8a1'), skill('Cursor', 'Cursor', '#fff')]],
  ['Tools & Others', 'Plan. Collaborate. Ship.', [skill('Git', 'Git', '#f65435'), skill('GitHub', 'Github', '#fff'), skill('VS Code', null, '#249ae9', 'VS'), skill('Notion', 'Notion', '#fff'), skill('Docker', 'Docker', '#289fee'), skill('Postman', 'Postman', '#ff6c37')]],
  ['Soft Skills', 'People. Ideas. Impact.', [
    { name: 'Problem Solving', component: Lightbulb }, { name: 'Communication', component: MessageSquare }, { name: 'Creativity', component: Sparkles }, { name: 'Teamwork', component: Users }, { name: 'Adaptability', component: ChartNoAxesCombined }
  ]]
];
function SkillItem({ item }) {
  const icon = icons['si' + item.slug]; const Symbol = item.component;
  const asset = { 'OpenAI': 'openai', 'CSS3': 'css3', 'VS Code': 'vscode' }[item.name];
  return <li><div className="skill-symbol" style={{ color: item.color || '#bf9b67' }} aria-hidden="true">
    {Symbol ? <Symbol strokeWidth={1.5} /> : asset ? <i className="skill-asset" style={{ maskImage: `url(public/skills/${asset}.svg)` }} /> : icon ? <svg viewBox="0 0 24 24" fill="currentColor"><path d={icon.path} /></svg> : <b>{item.fallback || item.name}</b>}
  </div><span>{item.name}</span></li>;
}
function SkillCategoryCard({ category, index }) {
  return <article className="skill-card" style={{ '--order': index }}><header><span className="skill-number">{String(index + 1).padStart(2, '0')}</span><h3>{category[0]}</h3><i /><p>{category[1]}</p></header><ul style={{ '--items': category[2].length }}>{category[2].map(item => <SkillItem key={item.name} item={item} />)}</ul></article>;
}
function SkillsHero() { return <header className="skills-heading"><h2 id="skillsTitle">Skills</h2><p className="skills-scene__subtitle">Tools that shape my vision</p></header>; }
function PortraitPanel() {
  return <div className="skills-photo">
    <img className="skills-scene-portrait" src="public/skills/skillme-face-corrected.JPEG" width="1920" height="1077" alt="A black-suit portrait in a sunset office, with one hand resting on the marble desk and the other in a pocket." loading="lazy" decoding="async" />
    <p className="skills-wall-note" aria-hidden="true">Skills turn ideas<br />into reality.</p>
    <div className="skills-portrait-caption" aria-hidden="true"><p>Good ideas build great things.</p><span>Discipline · Creativity · Consistency</span></div>
  </div>;
}
function SectionNavigation() { return <nav className="skills-navigation" aria-label="Continue portfolio"><a href="#projects">Explore projects <span aria-hidden="true">↗</span></a></nav>; }
function SkillsSection() {
  const ref = useRef(null);
  useEffect(() => {
    const section = ref.current.closest('.skills-scene');
    const media = matchMedia('(prefers-reduced-motion: reduce)');
    let frame = 0;
    const update = () => {
      frame = 0;
      if (media.matches) {
        section.style.removeProperty('--skills-slide');
        return;
      }
      // Horizontal translation leaves this vertical measurement unchanged.
      const top = section.getBoundingClientRect().top;
      const progress = Math.max(0, Math.min(1,
        (window.innerHeight - top) / (window.innerHeight * .82)));
      const eased = progress * progress * (3 - 2 * progress);
      section.style.setProperty('--skills-slide', `${(1 - eased) * 100}%`);
    };
    const schedule = () => { if (!frame) frame = requestAnimationFrame(update); };
    window.addEventListener('scroll', schedule, { passive: true });
    window.addEventListener('resize', schedule);
    media.addEventListener('change', schedule);
    update();
    return () => {
      cancelAnimationFrame(frame);
      window.removeEventListener('scroll', schedule);
      window.removeEventListener('resize', schedule);
      media.removeEventListener('change', schedule);
      section.style.removeProperty('--skills-slide');
    };
  }, []);
  useEffect(() => { const el = ref.current; const observer = new IntersectionObserver(([entry]) => { if (entry.isIntersecting) { el.classList.add('is-visible'); observer.disconnect(); } }, { threshold: .12 }); observer.observe(el); return () => observer.disconnect(); }, []);
  useEffect(() => { const el = ref.current; const media = matchMedia('(prefers-reduced-motion: reduce), (pointer: coarse)'); const move = e => { if (media.matches) return; const box = el.getBoundingClientRect(); el.style.setProperty('--portrait-shift', `${((e.clientX - box.left) / box.width - .5) * 3}px`); }; const reset = () => el.style.setProperty('--portrait-shift', '0px'); el.addEventListener('pointermove', move); el.addEventListener('pointerleave', reset); return () => { el.removeEventListener('pointermove', move); el.removeEventListener('pointerleave', reset); }; }, []);
  return <div className="skills-composition" ref={ref}><PortraitPanel /><div className="skills-scene__content"><SkillsHero /><div className="skills-grid">{categories.map((category, index) => <SkillCategoryCard key={category[0]} category={category} index={index} />)}</div></div><p className="skills-scene__script" aria-hidden="true">Same curiosity. A brighter tomorrow.</p><SectionNavigation /></div>;
}
createRoot(document.getElementById('skills')).render(<SkillsSection />);
