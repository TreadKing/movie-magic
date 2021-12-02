import React from 'react';
import PropTypes from 'prop-types';
import '../App.css';
import headerIllustrationDark from '../dist/images/header-illustration-dark.svg';
import heroMediaIllustrationDark from '../dist/images/hero-media-illustration-dark.svg';
import filmDark from '../dist/images/film-dark.png';
import feature01Light from '../dist/images/feature-01-light.svg';
import feature02Light from '../dist/images/feature-02-light.svg';
import feature03Light from '../dist/images/feature-03-light.svg';
import ScriptInjector from '../ScriptInjector';

function Landing({ doLogin }) {
  return (
    <>
      <div classNameName="body-wrap boxed-container">
        <header className="site-header" />

        <main>
          <section className="hero">
            <div className="container">
              <div className="hero-inner">
                <div className="hero-copy">
                  <h1 style={{ color: 'white' }} className="hero-title mt-0">Movie Magic</h1>
                  <p style={{ color: 'white' }} className="hero-paragraph">
                    Movie Magic is your own personalised watchlist of films you have
                    been waiting to watch all in one place.
                  </p>
                  <div className="hero-cta">
                    <button className="button button-primary" onClick={doLogin} type="button">Login</button>
                  </div>
                </div>
                <div className="hero-media">
                  <div className="header-illustration">
                    <img
                      src={headerIllustrationDark}
                      alt="Header illustration dark"
                    />
                  </div>
                  <div className="hero-media-illustration">
                    <img
                      className="hero-media-illustration-image asset-dark"
                      src={heroMediaIllustrationDark}
                      alt="Hero media illustration"
                    />
                  </div>
                  <div className="hero-media-container">
                    <img
                      className="hero-media-img"
                      src={filmDark}
                      alt="Hero media"
                    />
                  </div>
                </div>
              </div>
            </div>
          </section>

          <section className="features section">
            <div className="container">
              <div className="features-inner section-inner has-bottom-divider">
                <div className="features-header text-center">
                  <div className="container-sm">
                    <h2 className="hero-title mt-0" style={{ color: 'white' }}>Why Movie Magic?</h2>
                    <p className="hero-paragraph" style={{ color: 'white' }}>
                      With Movie Magic, you can get suggestions based on the
                      actors present in all your favorite film and save those
                      recommendations for later
                      reference, follow your friends and keep track of the
                      movies they plan to watch as
                      well.
                    </p>
                  </div>
                </div>
                <div className="features-wrap">
                  <div className="feature is-revealing">
                    <div className="feature-inner">
                      <div className="feature-icon">
                        <img
                          src={feature01Light}
                          alt="Feature 01"
                        />
                      </div>
                      <div className="feature-content">
                        <h3 style={{ color: 'white' }} className="feature-title mt-0">Search and Save Movies</h3>
                        <p style={{ color: 'white' }} className="text-sm mb-0">
                          Find and save movies you plan to watch on a personalized
                          watchlist.
                        </p>
                      </div>
                    </div>
                  </div>
                  <div className="feature is-revealing">
                    <div className="feature-inner">
                      <div className="feature-icon">
                        <img
                          src={feature02Light}
                          alt="Feature 02"
                        />
                      </div>
                      <div className="feature-content">
                        <h3 style={{ color: 'white' }} className="feature-title mt-0">Keep up with Friends</h3>
                        <p style={{ color: 'white' }} className="text-sm mb-0">
                          Keep up with the watchlists of your friends and allow
                          them to view your list as well.
                        </p>
                      </div>
                    </div>
                  </div>
                  <div className="feature is-revealing">
                    <div className="feature-inner">
                      <div className="feature-icon">
                        <img
                          src={feature03Light}
                          alt="Feature 03"
                        />
                      </div>
                      <div className="feature-content">
                        <h3 style={{ color: 'white' }} className="feature-title mt-0">Upcoming Releases</h3>
                        <p style={{ color: 'white' }} className="text-sm mb-0">
                          Get an updated list of upcoming movies for your viewing.
                        </p>
                        <br />
                        <br />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <section className="cta section">
            <div className="container-sm">
              <div className="cta-inner section-inner">
                <div className="cta-header text-center">
                  <h2 className="section-title mt-0" style={{ color: 'white' }}>The Creators</h2>
                  <p className="section-paragraph" style={{ color: 'white' }}>The app was created by the following developers:</p>
                  <li style={{ color: 'white' }}>Nana Krampah</li>
                  <li style={{ color: 'white' }}>Brandon Hodges</li>
                  <li style={{ color: 'white' }}>Devang Patel</li>
                  <li style={{ color: 'white' }}>Steven Maharath </li>
                  <br />
                  <br />
                  <div className="cta-cta">
                    <button className="button-primary" onClick={doLogin} type="button">Login Now</button>
                  </div>
                </div>
              </div>
            </div>
          </section>
        </main>

        <footer className="site-footer has-top-divider">
          <div className="container">
            <div className="site-footer-inner">

              <br />
              <br />
              <div className="footer-copyright">&copy; 2021 Movie Magic, all rights reserved</div>
            </div>
          </div>
        </footer>
      </div>
      <ScriptInjector />

    </>
  );
}

Landing.propTypes = {
  doLogin: PropTypes.func.isRequired,
};

export default Landing;
