import React from 'react';
import renderer from 'react-test-renderer';
import MovieSearch from './MovieSearch';

it('Test if the search page renders', () => {
  const component = renderer.create(<MovieSearch authToken=";)" />);
  const tree = component.toJSON();
  expect(tree).toMatchSnapshot();
});
