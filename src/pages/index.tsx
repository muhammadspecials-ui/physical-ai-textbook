import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import styles from './index.module.css';

function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <header className={styles.heroBanner}>
      <div className={styles.heroContent}>
        <div className={styles.heroText}>
          <span className={styles.badge}>🚀 AI-Powered Learning</span>
          <Heading as="h1" className={styles.heroTitle}>
            Master Physical AI &<br />Humanoid Robotics
          </Heading>
          <p className={styles.heroSubtitle}>
            Build intelligent robots with ROS 2, NVIDIA Isaac, and cutting-edge AI.
            From simulation to deployment, learn everything you need.
          </p>
          <div className={styles.heroButtons}>
            <Link className={styles.primaryButton} to="/docs/intro">
              Start Learning
              <span className={styles.buttonIcon}>→</span>
            </Link>
            <Link className={styles.secondaryButton} to="/signup">
              Create Account
              <span className={styles.buttonIcon}>✨</span>
            </Link>
          </div>
          <div className={styles.stats}>
            <div className={styles.stat}>
              <div className={styles.statNumber}>4</div>
              <div className={styles.statLabel}>Modules</div>
            </div>
            <div className={styles.stat}>
              <div className={styles.statNumber}>50+</div>
              <div className={styles.statLabel}>Lessons</div>
            </div>
            <div className={styles.stat}>
              <div className={styles.statNumber}>AI</div>
              <div className={styles.statLabel}>Powered</div>
            </div>
          </div>
        </div>
        <div className={styles.heroVisual}>
          <div className={styles.floatingCard}>
            <div className={styles.cardIcon}>🤖</div>
            <div className={styles.cardTitle}>ROS 2</div>
            <div className={styles.cardDesc}>Robotic Nervous System</div>
          </div>
          <div className={`${styles.floatingCard} ${styles.card2}`}>
            <div className={styles.cardIcon}>🎮</div>
            <div className={styles.cardTitle}>Simulation</div>
            <div className={styles.cardDesc}>Gazebo & Unity</div>
          </div>
          <div className={`${styles.floatingCard} ${styles.card3}`}>
            <div className={styles.cardIcon}>🧠</div>
            <div className={styles.cardTitle}>AI Brain</div>
            <div className={styles.cardDesc}>NVIDIA Isaac</div>
          </div>
        </div>
      </div>
    </header>
  );
}

function HomepageFeatures() {
  const features = [
    {
      icon: '🤖',
      title: 'ROS 2 Mastery',
      description: 'Master the robotic nervous system powering modern robots. Learn nodes, topics, services, and URDF.',
      gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    },
    {
      icon: '🎮',
      title: 'Simulation First',
      description: 'Test in Gazebo and Unity before deploying. Build digital twins with realistic physics.',
      gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    },
    {
      icon: '🧠',
      title: 'AI-Powered',
      description: 'Integrate GPT models and computer vision. Build robots that see, think, and act.',
      gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    },
    {
      icon: '🗣️',
      title: 'Voice Control',
      description: 'Natural language commands with Whisper and GPT-4. Make robots understand speech.',
      gradient: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
    },
    {
      icon: '👁️',
      title: 'Computer Vision',
      description: 'Object detection, tracking, and visual perception. Give robots the power to see.',
      gradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
    },
    {
      icon: '🎯',
      title: 'Capstone Project',
      description: 'Build an autonomous humanoid from scratch. Apply everything you learned.',
      gradient: 'linear-gradient(135deg, #30cfd0 0%, #330867 100%)',
    },
  ];

  return (
    <section className={styles.features}>
      <div className={styles.container}>
        <div className={styles.sectionHeader}>
          <h2 className={styles.sectionTitle}>Everything You Need</h2>
          <p className={styles.sectionSubtitle}>
            A complete curriculum designed for the future of robotics
          </p>
        </div>
        <div className={styles.featuresGrid}>
          {features.map((feature, idx) => (
            <div key={idx} className={styles.featureCard}>
              <div className={styles.featureIcon} style={{ background: feature.gradient }}>
                {feature.icon}
              </div>
              <h3 className={styles.featureTitle}>{feature.title}</h3>
              <p className={styles.featureDescription}>{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function HomepageCTA() {
  return (
    <section className={styles.ctaSection}>
      <div className={styles.ctaContent}>
        <h2 className={styles.ctaTitle}>Ready to Build the Future?</h2>
        <p className={styles.ctaSubtitle}>
          Join thousands of developers learning Physical AI and Humanoid Robotics
        </p>
        <div className={styles.ctaButtons}>
          <Link className={styles.ctaPrimary} to="/signup">
            Get Started Free
          </Link>
          <Link className={styles.ctaSecondary} to="/docs/intro">
            View Curriculum
          </Link>
        </div>
      </div>
    </section>
  );
}

export default function Home(): JSX.Element {
  const { siteConfig } = useDocusaurusContext();
  return (
    <Layout
      title="Home"
      description="Master Physical AI and Humanoid Robotics with ROS 2, NVIDIA Isaac, and GPT integration">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
        <HomepageCTA />
      </main>
    </Layout>
  );
}
