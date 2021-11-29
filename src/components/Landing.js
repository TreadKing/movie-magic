import React from 'react';

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
							</div>
						</div>
						<div className="hero-media">
							<div className="header-illustration">
								<img className="header-illustration-image asset-light"
									src="dist/images/header-illustration-light.svg" alt="Header illustration"/>
								<img className="header-illustration-image asset-dark"
									src="dist/images/header-illustration-dark.svg" alt="Header illustration"/>
							</div>
							<div className="hero-media-illustration">
								<img className="hero-media-illustration-image asset-light"
									src="dist/images/hero-media-illustration-light.svg" alt="Hero media illustration"/>
								<img className="hero-media-illustration-image asset-dark"
									src="dist/images/hero-media-illustration-dark.svg" alt="Hero media illustration"/>
							</div>
							<div className="hero-media-container">
								<img className="hero-media-image asset-light" src="dist/images/film-light.png"
									alt="Hero media"/>
								<img className="hero-media-image asset-dark" src="dist/images/film-dark.png"
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
										src="dist/images/features-illustration-dark.svg" alt="Feature illustration" />
									<img className="features-box asset-dark" src="dist/images/popcorn-dark.png"
										alt="Feature box" />
									<img className="features-illustration asset-dark"
										src="dist/images/features-illustration-top-dark.svg"
										alt="Feature illustration top" />
									<img className="features-illustration asset-light"
										src="dist/images/features-illustration-light.svg" alt="Feature illustration" />
									<img className="features-box asset-light" src="dist/images/popcorn-light.png"
										alt="Feature box" />
									<img className="features-illustration asset-light"
										src="dist/images/features-illustration-top-light.svg"
										alt="Feature illustration top" />
								</div>
							</div>
						</div>
						<div className="features-wrap">
							<div className="feature is-revealing">
								<div className="feature-inner">
									<div className="feature-icon">
										<img className="asset-light" src="dist/images/feature-01-light.svg"
											alt="Feature 01" />
										<img className="asset-dark" src="dist/images/feature-01-dark.svg" alt="Feature 01" />
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
										<img className="asset-light" src="dist/images/feature-02-light.svg"
											alt="Feature 02" />
										<img className="asset-dark" src="dist/images/feature-02-dark.svg" alt="Feature 02" />
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
										<img className="asset-light" src="dist/images/feature-03-light.svg"
											alt="Feature 03" />
										<img className="asset-dark" src="dist/images/feature-03-dark.svg" alt="Feature 03" />
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
								<a className="button button-primary" href="{{ url_for(bp.login) }}">Login Now</a>
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

    </>)
}

export default Landing;