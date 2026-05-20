const DATA_PATHS = {
  about: './data/aboutMeData.json',
  projects: './data/projectsData.json',
};

const FALLBACKS = {
  bio: 'This developer enjoys building accessible interfaces, learning new tools, and turning ideas into usable web experiences.',
  headshot: './images/headshot.webp',
  cardImage: './images/card_placeholder_bg.webp',
  spotlightImage: './images/spotlight_placeholder_bg.webp',
  projectName: 'Untitled Project',
  shortDescription: 'Project details are being prepared.',
  longDescription: 'More information about this project will be available soon.',
  url: '#',
};

const MAX_MESSAGE_LENGTH = 300;

const getValue = (value, fallback) => {
  if (typeof value === 'string' && value.trim()) {
    return value;
  }

  return fallback;
};

const resolveAssetPath = (path) => getValue(path, '').replace('../images/', './images/') || path;

const fetchJson = async (path) => {
  const response = await fetch(path);

  if (!response.ok) {
    throw new Error(`Unable to fetch ${path}`);
  }

  return response.json();
};

const createElement = (tag, options = {}) => {
  const element = document.createElement(tag);
  const { text, className, id, attributes = {} } = options;

  if (text) {
    element.textContent = text;
  }

  if (className) {
    element.className = className;
  }

  if (id) {
    element.id = id;
  }

  Object.entries(attributes).forEach(([name, value]) => {
    element.setAttribute(name, value);
  });

  return element;
};

const setBackgroundImage = (element, imagePath) => {
  element.style.backgroundImage = `url('${imagePath}')`;
  element.style.backgroundSize = 'cover';
  element.style.backgroundPosition = 'center';
};

const renderAboutMe = (aboutData) => {
  const aboutMe = document.querySelector('#aboutMe');
  const fragment = document.createDocumentFragment();
  const bio = createElement('p', {
    text: getValue(aboutData.aboutMe, FALLBACKS.bio),
  });
  const headshotContainer = createElement('div', {
    className: 'headshotContainer',
  });
  const headshot = createElement('img', {
    attributes: {
      src: resolveAssetPath(getValue(aboutData.headshot, FALLBACKS.headshot)),
      alt: 'Portfolio headshot for the featured developer',
    },
  });

  headshot.addEventListener('error', () => {
    headshot.src = FALLBACKS.headshot;
  }, { once: true });

  headshotContainer.appendChild(headshot);
  fragment.append(bio, headshotContainer);
  aboutMe.replaceChildren(fragment);
};

const normalizeProject = (project, index) => ({
  project_id: getValue(project.project_id, `project_${index + 1}`),
  project_name: getValue(project.project_name, FALLBACKS.projectName),
  short_description: getValue(project.short_description, FALLBACKS.shortDescription),
  long_description: getValue(project.long_description, FALLBACKS.longDescription),
  card_image: resolveAssetPath(getValue(project.card_image, FALLBACKS.cardImage)),
  spotlight_image: resolveAssetPath(getValue(project.spotlight_image, FALLBACKS.spotlightImage)),
  url: getValue(project.url, FALLBACKS.url),
});

const updateSpotlight = (project) => {
  const spotlight = document.querySelector('#projectSpotlight');
  const titles = document.querySelector('#spotlightTitles');
  const heading = createElement('h3', { text: project.project_name });
  const description = createElement('p', { text: project.long_description });
  const link = createElement('a', {
    text: 'Click here to see more...',
    attributes: {
      href: project.url,
      target: project.url === '#' ? '_self' : '_blank',
      rel: 'noopener',
    },
  });

  setBackgroundImage(spotlight, project.spotlight_image);
  titles.replaceChildren(heading, description, link);
};

const setActiveCard = (selectedCard) => {
  document.querySelectorAll('.projectCard').forEach((card) => {
    const isSelected = card === selectedCard;
    card.classList.toggle('active', isSelected);
    card.classList.toggle('inactive', !isSelected);
  });
};

const createProjectCard = (project) => {
  const card = createElement('div', {
    className: 'projectCard inactive',
    id: project.project_id,
    attributes: {
      role: 'button',
      tabindex: '0',
      'aria-label': `Show details for ${project.project_name}`,
    },
  });
  const title = createElement('h4', { text: project.project_name });
  const description = createElement('p', { text: project.short_description });

  setBackgroundImage(card, project.card_image);
  card.append(title, description);

  const selectProject = () => {
    updateSpotlight(project);
    setActiveCard(card);
  };

  card.addEventListener('click', selectProject);
  card.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      selectProject();
    }
  });

  return card;
};

const renderProjects = (projectsData) => {
  const projectList = document.querySelector('#projectList');
  const projects = projectsData.map(normalizeProject);
  const fragment = document.createDocumentFragment();

  projects.forEach((project) => {
    fragment.appendChild(createProjectCard(project));
  });

  projectList.replaceChildren(fragment);

  if (projects.length > 0) {
    updateSpotlight(projects[0]);
    setActiveCard(document.querySelector(`#${projects[0].project_id}`));
  }
};

const setupProjectScrolling = () => {
  const projectList = document.querySelector('#projectList');
  const leftArrow = document.querySelector('.arrow-left');
  const rightArrow = document.querySelector('.arrow-right');

  const getScrollAmount = () => {
    const firstCard = projectList.querySelector('.projectCard');
    return firstCard ? firstCard.getBoundingClientRect().width + 24 : 220;
  };

  const scrollProjects = (direction) => {
    const isDesktop = window.matchMedia('(min-width: 1024px)').matches;
    const distance = getScrollAmount() * direction;

    projectList.scrollBy({
      left: isDesktop ? 0 : distance,
      top: isDesktop ? distance : 0,
      behavior: 'smooth',
    });
  };

  leftArrow.addEventListener('click', () => scrollProjects(-1));
  rightArrow.addEventListener('click', () => scrollProjects(1));
};

const setError = (element, message) => {
  element.textContent = message;
};

const validateEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const invalidCharacterRegex = /[^a-zA-Z0-9@._-]/;

  if (!email) {
    return 'Please enter an email address.';
  }

  if (invalidCharacterRegex.test(email)) {
    return 'Email can only include letters, numbers, @, dots, underscores, and hyphens.';
  }

  if (!emailRegex.test(email)) {
    return 'Please enter a valid email address, such as name@example.com.';
  }

  return '';
};

const validateMessage = (message) => {
  const illegalMessageRegex = /[<>[\]{}]/;

  if (!message) {
    return 'Please enter a message.';
  }

  if (message.length > MAX_MESSAGE_LENGTH) {
    return 'Please keep your message at 300 characters or fewer.';
  }

  if (illegalMessageRegex.test(message)) {
    return 'Please remove brackets or angle brackets from your message.';
  }

  return '';
};

const updateCharacterCount = () => {
  const messageInput = document.querySelector('#contactMessage');
  const counter = document.querySelector('#charactersLeft');
  const remaining = MAX_MESSAGE_LENGTH - messageInput.value.length;

  counter.textContent = `Characters remaining: ${remaining}/300`;
  counter.classList.toggle('error', remaining < 0);
  counter.style.color = remaining < 0 ? 'var(--error)' : 'inherit';
};

const setupFormValidation = () => {
  const form = document.querySelector('#formSection');
  const emailInput = document.querySelector('#contactEmail');
  const messageInput = document.querySelector('#contactMessage');
  const emailError = document.querySelector('#emailError');
  const messageError = document.querySelector('#messageError');

  updateCharacterCount();
  messageInput.addEventListener('input', updateCharacterCount);

  form.addEventListener('submit', (event) => {
    event.preventDefault();

    const emailMessage = validateEmail(emailInput.value.trim());
    const contactMessage = validateMessage(messageInput.value.trim());

    setError(emailError, emailMessage);
    setError(messageError, contactMessage);

    if (!emailMessage && !contactMessage) {
      alert('Your message was submitted correctly and validation was successful.');
      form.reset();
      updateCharacterCount();
    }
  });
};

const initializePortfolio = async () => {
  try {
    const [aboutData, projectsData] = await Promise.all([
      fetchJson(DATA_PATHS.about),
      fetchJson(DATA_PATHS.projects),
    ]);

    renderAboutMe(aboutData);
    renderProjects(projectsData);
    setupProjectScrolling();
    setupFormValidation();
  } catch (error) {
    console.error(error);
  }
};

document.addEventListener('DOMContentLoaded', initializePortfolio);
