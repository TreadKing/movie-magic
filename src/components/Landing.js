import React from 'react';
// import '../dist/css/style.css'
import header_illustration_light from '../dist/images/header-illustration-light.svg'
import header_illustration_dark from '../dist/images/header-illustration-dark.svg'
import hero_media_illustration_light from '../dist/images/hero-media-illustration-light.svg'
import hero_media_illustration_dark from '../dist/images/hero-media-illustration-dark.svg'
import film_light from '../dist/images/film-light.png'
import film_dark from '../dist/images/film-dark.png'
import features_illustration_dark from  '../dist/images/features-illustration-dark.svg'
import popcorn_dark from '../dist/images/popcorn-dark.png'
import features_illustration_top_dark from '../dist/images/features-illustration-top-dark.svg'
import features_illustration_light from '../dist/images/features-illustration-light.svg'
import popcorn_light from '../dist/images/popcorn-light.png'
import features_illustration_top_light from '../dist/images/features-illustration-top-light.svg'
import feature_01_light from '../dist/images/feature-01-light.svg'
import feature_01_dark from '../dist/images/feature-01-dark.svg'
import feature_02_light from '../dist/images/feature-02-light.svg'
import feature_02_dark from '../dist/images/feature-02-dark.svg'
import feature_03_light from '../dist/images/feature-03-light.svg'
import feature_03_dark from '../dist/images/feature-03-dark.svg'
import ScriptInjector from '../ScriptInjector';


function Landing({ doLogin }) {
    return (
    <>
    <div classNameName="body-wrap boxed-container">
		<header className="site-header">
		</header>

		<main>
			<section className="hero">
				<div className="container">
					<div className="hero-inner">
						<div className="hero-copy">
							<h1 className="hero-title mt-0">Movie Magic</h1>
							<p className="hero-paragraph">Movie Magic is your own personalised watchlist of films you have
								been waiting to watch all in one place.</p>
							<div className="hero-cta">
								<button className="button button-primary" onClick={doLogin}>Login</button>
								<div class="lights-toggle">
									<input id="lights-toggle" type="checkbox" name="lights-toggle" class="switch"
										checked="checked" />
									<label for="lights-toggle" class="text-xs"><span>Turn me <span
												class="label-text">dark</span></span></label>
								</div>
							</div>
						</div>
						<div className="hero-media">
							<div className="header-illustration">
								<img className="header-illustration-image asset-light"
									src={ header_illustration_light } alt="Header illustration light"/>
								<img className="header-illustration-image asset-dark"
									src={ header_illustration_dark } alt="Header illustration dark"/>
							</div>
							<div className="hero-media-illustration">
								<img className="hero-media-illustration-image asset-light"
									src={ hero_media_illustration_light } alt="Hero media illustration"/>
								<img className="hero-media-illustration-image asset-dark"
									src={ hero_media_illustration_dark } alt="Hero media illustration"/>
							</div>
							<div className="hero-media-container">
								<img className="hero-media-image asset-light" src={ film_light }
									alt="Hero media"/>
								<img className="hero-media-image asset-dark" src={ film_dark }
									alt="Hero media"/>
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
								<h2 className="section-title mt-0">Why Movie Magic?</h2>
								<p className="section-paragraph">With Movie Magic, you can get suggestions based on the
									actors present in all your favourite film and save those recommendations for later
									reference, follow your friends and keep track of the movies they plan to watch as
									well.
								</p>
								<div className="features-image">
									<img className="features-illustration asset-dark"
										src={ features_illustration_dark } alt="Feature illustration" />
									<img className="features-box asset-dark" src={ popcorn_dark }
										alt="Feature box" />
									<img className="features-illustration asset-dark"
										src={ features_illustration_top_dark }
										alt="Feature illustration top" />
									<img className="features-illustration asset-light"
										src={ features_illustration_light } alt="Feature illustration" />
									<img className="features-box asset-light" src={ popcorn_light }
										alt="Feature box" />
									<img className="features-illustration asset-light"
										src={ features_illustration_top_light }
										alt="Feature illustration top" />
								</div>
							</div>
						</div>
						<div className="features-wrap">
							<div className="feature is-revealing">
								<div className="feature-inner">
									<div className="feature-icon">
										<img className="asset-light" src={ feature_01_light }
											alt="Feature 01" />
										<img className="asset-dark" src={ feature_01_dark } alt="Feature 01" />
									</div>
									<div className="feature-content">
										<h3 className="feature-title mt-0">Search and Save Movies</h3>
										<p className="text-sm mb-0">Find and save movies you plan to watch on a personalised
											watchlist.</p>
									</div>
								</div>
							</div>
							<div className="feature is-revealing">
								<div className="feature-inner">
									<div className="feature-icon">
										<img className="asset-light" src={ feature_02_light }
											alt="Feature 02" />
										<img className="asset-dark" src={ feature_02_dark } alt="Feature 02" />
									</div>
									<div className="feature-content">
										<h3 className="feature-title mt-0">Keep up with Friends</h3>
										<p className="text-sm mb-0">Keep up with the watchlists of your friends and allow
											them to view your list as well.</p>
									</div>
								</div>
							</div>
							<div className="feature is-revealing">
								<div className="feature-inner">
									<div className="feature-icon">
										<img className="asset-light" src={ feature_03_light }
											alt="Feature 03" />
										<img className="asset-dark" src={ feature_03_dark } alt="Feature 03" />
									</div>
									<div className="feature-content">
										<h3 className="feature-title mt-0">Upcoming Releases</h3>
										<p className="text-sm mb-0">Get an updated list of upcoming movies for your viewing.
										</p>
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
							<h2 className="section-title mt-0">The Creators</h2>
							<p className="section-paragraph">The app was created by the following developers:</p>
							<li>Nana Krampah</li>
							<li>Brandon Hodges</li>
							<li>Devang Patel</li>
							<li>Steven Maharath </li>
							<br />
							<div className="cta-cta">
								<button className="button button-primary" onClick={ doLogin }>Login Now</button>
							</div>
						</div>
					</div>
				</div>
			</section>
		</main>

		<footer className="site-footer has-top-divider">
			<div className="container">
				<div className="site-footer-inner">


					<div className="footer-copyright">&copy; 2021 Movie Magic, all rights reserved</div>
				</div>
			</div>
		</footer>
	</div>
	<ScriptInjector />

    </>)
}

export default Landing;