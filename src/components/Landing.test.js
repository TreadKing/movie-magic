import React from 'react';
import renderer from 'react-test-renderer';
import Landing from './Landing';

it('Test if the landing page renders', () => {
  const component = renderer.create(<Landing doLogin={() => {}} />);
  const tree = component.toJSON();
  expect(tree).toMatchSnapshot();
});
