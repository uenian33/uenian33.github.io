#!/usr/bin/env python3
"""Generate the static homepage (index.html) from the publication data below.

Usage: python3 tools/build_index.py   (run from anywhere; writes ../index.html)
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ICON = {'OpenReview': '📝', 'Patent': '📑', 'Paper': '📄', 'arXiv': '📜', 'Code': '💻', 'Project': '🌐', 'Dataset': '🗂️', 'Video': '🎬'}


def pub(title, authors, venue, kind='Conference', vclass='', tldr='', img=None, video=None, links=(), small=False):
    media = ''
    if video:
        media += (f'<video autoplay muted loop playsinline preload="metadata" poster="videos/{video}.jpg">'
                  f'<source src="videos/{video}.mp4" type="video/mp4"></video>')
    if img:
        media += f'<img src="images/{img}" alt="" loading="lazy">'
    authors = re.sub(r'Wenyan Yang(\*?)', r'<strong>Wenyan Yang\1</strong>', authors)
    url = links[0][1] if links else None
    t = f'<a href="{url}">{title}</a>' if url else title
    btns = ''.join(f'<a class="btn" href="{u}">{ICON.get(n, "")} {n}</a>' for n, u in links)
    m = re.search(r'(19|20)\d{2}', venue)
    year = m.group(0) if m else '2026'
    return f'''<article class="pub{' small' if small else ''}" data-year="{year}" data-cat="__CAT__">
<div class="media">{media}</div>
<div class="pub-body">
<h3 class="pub-title">{t}</h3>
{f'<p class="authors">{authors}</p>' if authors else ''}
<div class="meta"><span class="venue {vclass}">{venue}</span><span class="type">{kind}</span></div>
{f'<p class="tldr">{tldr}</p>' if tldr else ''}
{f'<div class="links">{btns}</div>' if btns else ''}
</div>
</article>'''


REVIEW = dict(venue='Under review', kind='Manuscript', vclass='review')

ONGOING = [
    pub('Human-to-Any-Robot Motion Retargeting: One Learning-Free Retargeter for Arbitrary Morphologies', '',
        venue='Ongoing', kind='Research preview', vclass='ongoing',
        tldr='A single learning-free retargeter maps human motion and human-object interaction (CMU mocap, OMOMO) onto robots '
             'with very different bodies. The video shows the same human clips on a quadruped with two arms (ANYmal C + two Z1), '
             'Spot with an arm, a Unitree G1 humanoid and a differential-drive base with a Lite6 arm, across locomotion, '
             'gesture and object-carrying tasks.',
        video='retarget_any'),
    pub('From Onboard Cameras to Actions: A Language-Driven Spot Agent with Semantic Scene Memory', '',
        venue='Ongoing', kind='Research preview', vclass='ongoing',
        tldr='Spot explores a kitchen with its own body and arm cameras, fuses the views into a semantic map and an object '
             'memory, and a vision-language planner calls walking, looking and grasping skills as tools to finish a spoken task '
             '(here: “pick up the donut”). Developed in simulation with Spot’s real camera rig, for transfer to the real robot.',
        video='spot_agent'),
]

ROBOT = [
    pub('CroMoGen: Cross-Morphology Demonstration Retargeting for Mobile Manipulation',
        'Jaakko Tuomisto*, Wenyan Yang*, Joni Pajarinen', **REVIEW,
        tldr='One human or robot demonstration is retargeted into executed whole-body mobile-manipulation demonstrations '
             'for robots with very different bodies: Spot, Panda-Omron and Unitree G1 in simulation, and Spot in the real world. '
             '(* equal contribution)',
        img='pubs/cromogen.png', video='cromogen'),
    pub('Why Cross-Skeleton Retargeting Is Non-Identifiable: Structural Limits of Generative Motion Models',
        'Zhiyuan Li, Wenyan Yang, Pekka Marttinen, Joni Pajarinen', 'NeurIPS 2026',
        tldr='Under standard generative objectives, sparse multi-body motion data cannot pin down which source-to-target map '
             'a cross-skeleton retargeting model learns. We propose Source-Instance Fidelity (SIF) to test whether a generated '
             'motion actually follows its source clip, across humanoid robots and animation skeletons.',
        img='pubs/xskel.png', video='xskel',
        links=[('Paper', 'https://arxiv.org/abs/2609.37297'),
               ('Code', 'https://github.com/LiZhYun/NeurIPS2026-Cross-Skeleton-Retargeting'),
               ('Project', 'https://cross-skeleton-retargeting.netlify.app/')]),
    pub('Extracting Visual Plans from Unlabeled Videos via Symbolic Guidance',
        'Wenyan Yang, Ahmet Tikna, Yi Zhao, Yuying Zhang, Luigi Palopoli, Marco Roveri, Joni Pajarinen', 'CoRL 2025',
        tldr='Vis2Plan: vision foundation models turn unlabeled play data into symbolic task states; a symbolic planner then '
             'guides fast, physically consistent visual subgoal plans for long-horizon manipulation, in simulation and on a real Spot.',
        img='pubs/vis2plan.png', video='vis2plan',
        links=[('Paper', 'https://proceedings.mlr.press/v305/yang25c.html'), ('arXiv', 'https://arxiv.org/abs/2505.08444'),
               ('Project', 'https://sites.google.com/view/vis2plan/home')]),
    pub('ReMoBot: Retrieval-Based Few-Shot Imitation Learning for Mobile Manipulation',
        'Yuying Zhang, Wenyan Yang, Francesco Verdoja, Ville Kyrki, Joni Pajarinen', 'AIM 2026',
        tldr='With only 20 demonstrations and no extra training, a Spot robot solves mobile manipulation tasks by retrieving '
             'the most relevant demonstrated trajectories with vision-foundation-model features and replaying their actions. '
             'An earlier version appeared at the CoRL 2025 RemembeRL Workshop.',
        img='pubs/remobot.png', video='remobot',
        links=[('Paper', 'https://ieeexplore.ieee.org/abstract/document/11658109/'),
               ('OpenReview', 'https://openreview.net/forum?id=k4jVv0KDDp'),
               ('arXiv', 'https://arxiv.org/abs/2408.15919'), ('Project', 'https://sites.google.com/view/remobot/home')]),
    pub('Learning Spatial Alignment for Underwater Robots with Limited Real-World Data',
        'Yang Weng, Yongxi Cao, Wenyan Yang, Motoki Sakai, Jinyu Tong, Hiroki Yokohata, Yuichi Motegi, Sehwa Chun, '
        'Joni Pajarinen, Toshihiro Maki', **REVIEW,
        tldr='An alignment policy for an autonomous underwater vehicle is trained in simulation and then improved with a '
             'small amount of real-world data, evaluated in sea trials and water-tank experiments.',
        img='pubs/underwater.png', video='underwater'),
    pub('Seq2Seq Imitation Learning for Tactile Feedback-based Manipulation',
        'Wenyan Yang, Alexandre Angleraud, Roel S. Pieters, Joni Pajarinen, Joni-Kristian Kämäräinen', 'ICRA 2023',
        img='wenyan_yang_seq2seq.png', links=[('Paper', 'https://arxiv.org/abs/2303.02646')], small=True),
    pub('Enhancing Cooperative Exploration and Planning: UAV-Legged Robot Synergy',
        'Zhengyang Li, Peng Xu, Liang Ding, Junqi Shan, Wenyan Yang, Zongquan Deng, Haibo Gao, Tie Liu, Huaiguang Yang',
        'RA-L 2024', kind='Journal', img='pubs/uav.png',
        tldr='A UAV explores unknown terrain and searches for targets while planning a route that a legged robot can actually '
             'traverse, validated in simulation and in field experiments with a UAV and a hexapod robot.',
        links=[('Paper', 'https://doi.org/10.1109/LRA.2024.3443597')], small=True),
    pub('Monolithic vs. Hybrid Controller for Multi-objective Sim-to-Real Learning',
        'Atakan Dag, Alexandre Angleraud, Wenyan Yang, Nataliya Strokina, Roel S. Pieters, Minna Lanz, Joni-Kristian Kämäräinen',
        'IROS 2021', img='wenyan_yang_hybrid.png', links=[('Paper', 'https://ieeexplore.ieee.org/document/9636426')], small=True),
    pub('Neural Network Controller for Autonomous Pile Loading Revised',
        'Wenyan Yang, Nataliya Strokina, Nikolay Serbenyuk, Joni Pajarinen, Reza Ghabcheloo, Juho Vihonen, Mohammad M. Aref, '
        'Joni-Kristian Kämäräinen', 'ICRA 2021', kind='Conference · Oral', img='wenyan_yang_nn_pile.png',
        links=[('Paper', 'https://ieeexplore.ieee.org/document/9561804')], small=True),
    pub('Learning a Pile Loading Controller from Demonstrations',
        'Wenyan Yang, Nataliya Strokina, Nikolay Serbenyuk, Reza Ghabcheloo, Joni Kämäräinen', 'ICRA 2020',
        kind='Conference · Oral', img='wenyan_yang_rf_pile.png',
        links=[('Paper', 'https://ieeexplore.ieee.org/document/9196907')], small=True),
    pub('Visual Rewards From Observation for Sequential Tasks: Autonomous Pile Loading',
        'Nataliya Strokina, Wenyan Yang, Joni Pajarinen, Nikolay Serbenyuk, Joni Kämäräinen, Reza Ghabcheloo',
        'Frontiers in Robotics and AI 2022', kind='Journal',
        links=[('Paper', 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9194444/')], small=True),
]

RL = [
    pub('SUN: Reaching for Novelty in Reinforcement Learning',
        'Wenyan Yang, Arsenii Mustafin, Dominik Baumann, Joni Pajarinen, Simone Parisi', **REVIEW,
        tldr='Novelty alone sends an agent to goals it cannot reach, and reachability alone gives no exploration. SUN is a '
             'single goal-selection indicator, built on successor value functions, that scores goals that are both novel and reachable.',
        img='pubs/sun.png', links=[('arXiv', 'https://arxiv.org/abs/2609.08642'), ('Code', 'https://github.com/sparisi/rl-anvil')]),
    pub('GCHR: Goal-Conditioned Hindsight Regularization for Sample-Efficient Reinforcement Learning',
        'Xing Lei, Wenyan Yang, Kaiqiang Ke, Shentao Yang, Xuetao Zhang, Joni Pajarinen, Donglin Wang', **REVIEW,
        tldr='Policy bootstrapping for goal-conditioned RL that regularizes the policy with two priors built from replayed '
             'experience: a self-imitation action prior and a hindsight goal prior.',
        img='pubs/gchr.png', links=[('arXiv', 'https://arxiv.org/abs/2508.06108')]),
    pub('Probabilistic Subgoal Representations for Hierarchical Reinforcement Learning',
        'Vivienne Huiling Wang, Tinghuai Wang, Wenyan Yang, Joni-Kristian Kämäräinen, Joni Pajarinen', 'ICML 2024',
        img='pubs/psr.png', links=[('Paper', 'https://arxiv.org/abs/2406.16707')], small=True),
    pub('Swapped Goal-conditioned Offline Reinforcement Learning',
        'Wenyan Yang, Huiling Wang, Dingding Cai, Joni Pajarinen, Joni-Kristian Kämäräinen', 'arXiv 2023', kind='Preprint',
        vclass='preprint', img='wenyan_yang_offline_gcrl.png', links=[('arXiv', 'https://arxiv.org/abs/2302.08865')], small=True),
    pub('Prioritized Offline Goal-swapping Experience Replay',
        'Wenyan Yang, Joni Pajarinen, Dingding Cai, Joni Kämäräinen', 'ICLR 2023 RRL', kind='Workshop', vclass='workshop',
        img='wenyan_yang_pger.png', links=[('Paper', 'https://arxiv.org/abs/2302.07741')], small=True),
    pub('Constrained Imitation Q-learning with Earth Mover’s Distance Reward',
        'Wenyan Yang, Nataliya Strokina, Joni Pajarinen, Joni-Kristian Kämäräinen', 'NeurIPS 2022', kind='Workshop',
        vclass='workshop', img='wenyan_yang_cemd.png', links=[('Paper', 'https://openreview.net/pdf?id=rzfPNkOyC7O')], small=True),
]

VISION = [
    pub('Smoothing Slot Attention Iterations and Recurrences',
        'Rongzhen Zhao, Wenyan Yang, Juho Kannala, Joni Pajarinen', 'ICML 2026',
        tldr='SmoothSA: object-centric learning groups the pixels of an image or video into object slots without labels. '
             'We smooth Slot Attention’s iterations and recurrences so that queries are informative from the first step, '
             'giving cleaner object segmentation on images and videos.',
        img='pubs/smoothsa.png', links=[('Paper', 'https://arxiv.org/abs/2508.05417'), ('Code', 'https://github.com/Genera1Z/SmoothSA')]),
    pub('Rethinking Temporal Consistency in Video Object-Centric Learning: From Prediction to Correspondence',
        'Zhiyuan Li, Rongzhen Zhao, Wenyan Yang, Wenshuai Zhao, Pekka Marttinen, Joni Pajarinen', 'ICML 2026',
        tldr='Keeping each object in the same slot across video frames is usually done with a learned temporal predictor. '
             'Seeding slots from saliency in frozen DINOv2 features and Hungarian-matching them across frames does the same job '
             'with no learned temporal parameters.',
        img='pubs/temporal.png',
        links=[('Paper', 'https://proceedings.mlr.press/v306/li26js.html'), ('arXiv', 'https://arxiv.org/abs/2605.03650'),
               ('Code', 'https://github.com/LiZhYun/ICML2026-RethinkingOCL')]),
    pub('Object Detection in Equirectangular Panorama',
        'Wenyan Yang, Yanlin Qian, Joni-Kristian Kämäräinen, Francesco Cricri, Lixin Fan', 'ICPR 2018', kind='Conference · Oral',
        img='wenyan_yang_360.png', links=[('Paper', 'https://arxiv.org/abs/1805.08009'),
                                           ('Dataset', 'https://github.com/uenian33/360_object_detection_dataset')], small=True),
]

PAGE = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Wenyan Yang</title>
<meta name="description" content="Wenyan Yang, postdoctoral researcher at the Robot Learning Lab, Aalto University: cross-morphology transfer, reinforcement learning and robot learning.">
<meta name="google-site-verification" content="lKr4HkjPyaLT60EFFaX_zTOEunaePov6FJmaMlvNkTw">
<link rel="icon" href="images/favicon-32x32.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,300;0,400;0,700;1,400&display=swap">
<link rel="stylesheet" href="assets/css/home.css">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-391WJPDDMM"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-391WJPDDMM');</script>
</head>
<body>
<nav class="nav"><div class="nav-in">
<a class="brand" href="#top">Wenyan Yang</a>
<a class="lnk" href="#top">Home</a>
<a class="lnk" href="#publications">Publications</a>
<a class="lnk opt" href="#projects">Projects</a>
</div></nav>
<main id="top">

<section class="card hero">
<div class="hero-text">
<h1>Wenyan Yang</h1>
<p class="role">🤖 Postdoctoral Researcher @ Robot Learning Lab, Aalto University &nbsp;·&nbsp; 📍 Espoo, Finland</p>
<p>I am a postdoctoral researcher at the <a href="https://rl.aalto.fi/">Aalto Robot Learning Lab</a>, Aalto University, working with Prof. Joni Pajarinen. I study how robots can learn skills from demonstrations and from their own exploration: <b>cross-morphology motion and demonstration transfer</b> (retargeting one demonstration to robots with different bodies), <b>reinforcement learning and exploration</b>, <b>imitation and offline reinforcement learning</b>, and <b>visual representation learning for manipulation</b>.</p>
<p>I received my Ph.D. from Tampere University, advised by Prof. Joni-Kristian Kämäräinen. Before that I worked as a research engineer at Cargotec on learning-based autonomous control of cranes and container handling.</p>
<div class="blk"><h4>📬 Social &amp; Contacts</h4><div class="chips">
<a class="chip" href="mailto:wenyan.yang@aalto.fi">wenyan.yang(at)aalto.fi</a>
<a class="chip" href="https://scholar.google.com/citations?user=0bTF5XUAAAAJ">Google Scholar</a>
<a class="chip" href="https://github.com/uenian33">GitHub</a>
<a class="chip" href="https://www.linkedin.com/in/wenyan-yang-523703268">LinkedIn</a>
<a class="chip" href="files/Wenyan_Yang_CV.pdf">CV</a>
</div></div>
<div class="blk"><h4>🔬 Research Interests</h4><div class="chips">
<span class="chip">Cross-Morphology Transfer</span><span class="chip">Reinforcement Learning &amp; Exploration</span>
<span class="chip">Imitation &amp; Offline RL</span><span class="chip">Robotic Manipulation</span><span class="chip">Visual Representation Learning</span>
</div></div>
</div>
<img class="avatar" src="images/avatar.jpg" alt="Portrait of Wenyan Yang">
</section>

<section class="card"><div class="cols">
<div>
<h2 class="sec">💼 Experience</h2>
<div class="row"><div class="what"><b>Aalto University</b><span>Postdoctoral Researcher, Robot Learning Lab · Prof. Joni Pajarinen</span></div><div class="when">Jun 2023 – Present</div></div>
<div class="row"><div class="what"><b>Cargotec Oyj</b><span>Research Engineer · learning-based autonomous crane control</span></div><div class="when">2019 – 2022</div></div>
<h2 class="sec" style="margin-top:22px">🎓 Education</h2>
<div class="row"><div class="what"><b>Tampere University</b><span>Ph.D., Computing and Electrical Engineering · Prof. Joni-Kristian Kämäräinen</span></div><div class="when">2019 – 2026</div></div>
<div class="row"><div class="what"><b>Tampere University of Technology</b><span>M.Sc., Human-Computer Interaction, with distinction</span></div><div class="when">2016 – 2019</div></div>
<div class="row"><div class="what"><b>Sichuan University</b><span>B.Eng., Computer Science</span></div><div class="when">2012 – 2016</div></div>
</div>
<div>
<h2 class="sec">🤝 Service</h2>
<ul class="plain">
<li><b>Associate Editor</b>, IROS 2025 and 2026</li>
<li><b>Co-organiser</b>, CoRL 2025 RemembeRL Workshop</li>
<li>Reviewer for ICML, AAAI, CoRL, ICRA and IROS</li>
<li>Organisation and evaluation, ECCV VOT2022 Challenge</li>
<li>Supervision of doctoral, master's and bachelor's student projects at Aalto University</li>
</ul>
<h2 class="sec" style="margin-top:22px">🧭 Funded Projects</h2>
<ul class="plain">
<li>XSCAVE (EU Horizon Europe, 101189836)</li>
<li>MARL (Research Council of Finland, 357301)</li>
<li>DSII industry-academia collaboration project, Finland</li>
</ul>
</div>
</div></section>

<section class="card" id="publications">
<h2 class="sec">📝 Publications <a class="chip" style="margin-left:auto;font-weight:400" href="https://scholar.google.com/citations?user=0bTF5XUAAAAJ">Google Scholar →</a></h2>
<div class="pubbar" id="pubbar" hidden>
<div class="seg" role="group" aria-label="Sort publications by"><span class="seg-label">Sort by</span>
<button type="button" data-sort="category" class="on">Category</button><button type="button" data-sort="year">Year</button></div>
<div class="tabs" id="cat-tabs" role="tablist" aria-label="Publication category">
<button type="button" role="tab" data-cat="all" class="on">All</button>
<button type="button" role="tab" data-cat="ongoing">On-going Research</button>
<button type="button" role="tab" data-cat="robot">Robot Learning</button>
<button type="button" role="tab" data-cat="rl">Reinforcement Learning</button>
<button type="button" role="tab" data-cat="vision">Visual Representation</button>
</div>
</div>
<div id="publist">
<h3 class="sub">On-going Research</h3>
__ONGOING__
<h3 class="sub">Cross-Morphology Transfer and Robot Learning</h3>
__ROBOT__
<h3 class="sub">Reinforcement Learning and Exploration</h3>
__RL__
<h3 class="sub">Visual Representation Learning</h3>
__VISION__
</div>
</section>

<section class="card" id="projects">
<h2 class="sec">🛠️ Projects &amp; Patent</h2>
<article class="pub">
<div class="media"><video autoplay muted loop playsinline preload="metadata" poster="videos/crane.jpg"><source src="videos/crane.mp4" type="video/mp4"></video></div>
<div class="pub-body">
<h3 class="pub-title"><a href="https://patents.google.com/patent/WO2022008793A1/en">Autonomous Industrial Crane Controller: Relative Positioning of a Container Spreader</a></h3>
<p class="authors"><strong>Wenyan Yang</strong>, Mohammad Aref, Juho Vihonen, Jyri Lukkala, Mikko Asikainen, Hannu Santahuhta</p>
<div class="meta"><span class="venue">WO Patent 2022</span><span class="type">Cargotec · DSII project · 2019 – 2022</span></div>
<p class="tldr">A learning-based controller that positions a crane's spreader relative to a container from the spreader's own corner cameras (shown in the video), so that containers can be picked and placed autonomously. The work resulted in patent WO2022008793A1 and a solution delivered on real cranes.</p>
<div class="links"><a class="btn" href="https://patents.google.com/patent/WO2022008793A1/en">📑 Patent</a></div>
</div>
</article>
<div class="proj"><b>360° Video Object Detection</b><span class="when">Nokia · 2017 – 2018</span>
<p>Object detection in 360° videos for the Nokia OZO camera, with a panoramic object detection <a href="https://github.com/uenian33/360_object_detection_dataset">dataset</a> and a YOLO-based baseline.</p></div>
<div class="proj"><b>Depth Image Data Augmentation</b>
<p>A Python library that generates SGM-style stereo disparity maps from a single RGB image, for augmenting data to look like real depth-camera images. <a href="https://github.com/uenian33/mono2SGM">Code</a></p></div>
<div class="proj"><b>General Grasping Controller for Motoman NX100</b>
<p>A depth-image-based grasp pose estimator for the Motoman NX100. <a href="https://github.com/uenian33/nx100_robotic_tasks">Code</a> · <a href="https://www.youtube.com/watch?v=NBE9e7AJw6I">Video</a></p></div>
<div class="proj"><b>VOT2022 Challenge</b>
<p>Co-author of <a href="https://link.springer.com/chapter/10.1007/978-3-031-25085-9_25">The Tenth Visual Object Tracking VOT2022 Challenge Results</a> (ECCV 2022 Workshops).</p></div>
</section>

<footer>© Wenyan Yang · Last updated November 2026</footer>
</main>
<script>
(function () {
  var list = document.getElementById('publist'), bar = document.getElementById('pubbar');
  if (!list || !bar) return;
  var pubs = [].slice.call(list.querySelectorAll('.pub'));
  var CATS = [['ongoing', 'On-going Research'], ['robot', 'Cross-Morphology Transfer and Robot Learning'], ['rl', 'Reinforcement Learning and Exploration'], ['vision', 'Visual Representation Learning']];
  var sort = 'category', cat = 'all';
  var tabs = document.getElementById('cat-tabs');
  function head(t) { var h = document.createElement('h3'); h.className = 'sub'; h.textContent = t; return h; }
  function count(c) { return pubs.filter(function (p) { return c === 'all' || p.dataset.cat === c; }).length; }
  [].forEach.call(tabs.querySelectorAll('button'), function (b) {
    var n = document.createElement('span'); n.className = 'n'; n.textContent = count(b.dataset.cat); b.appendChild(n);
  });
  function render() {
    var out = [];
    if (sort === 'year') {
      var years = pubs.map(function (p) { return p.dataset.year; }).filter(function (y, i, a) { return a.indexOf(y) === i; }).sort().reverse();
      years.forEach(function (y) { out.push(head(y)); pubs.forEach(function (p) { if (p.dataset.year === y) out.push(p); }); });
    } else {
      CATS.forEach(function (c) {
        if (cat !== 'all' && cat !== c[0]) return;
        if (cat === 'all') out.push(head(c[1]));
        pubs.forEach(function (p) { if (p.dataset.cat === c[0]) out.push(p); });
      });
    }
    while (list.firstChild) list.removeChild(list.firstChild);
    out.forEach(function (n) { list.appendChild(n); });
    tabs.hidden = sort !== 'category';
    [].forEach.call(bar.querySelectorAll('[data-sort]'), function (b) { b.classList.toggle('on', b.dataset.sort === sort); });
    [].forEach.call(tabs.querySelectorAll('button'), function (b) { b.classList.toggle('on', b.dataset.cat === cat); b.setAttribute('aria-selected', b.dataset.cat === cat); });
    [].forEach.call(list.querySelectorAll('video'), function (v) { var p = v.play(); if (p && p.catch) p.catch(function () {}); });
  }
  bar.addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (!b) return;
    if (b.dataset.sort) sort = b.dataset.sort;
    if (b.dataset.cat) cat = b.dataset.cat;
    render();
  });
  bar.hidden = false;
  render();
})();
</script>
</body>
</html>
'''

def group(items, cat):
    return '\n'.join(items).replace('__CAT__', cat)


html = (PAGE.replace('__ONGOING__', group(ONGOING, 'ongoing')).replace('__ROBOT__', group(ROBOT, 'robot')).replace('__RL__', group(RL, 'rl')).replace('__VISION__', group(VISION, 'vision')))
html = re.sub(r'<div class="media"></div>\n', '', html)
(ROOT / 'index.html').write_text(html, encoding='utf-8')
print('wrote', ROOT / 'index.html', len(html))
