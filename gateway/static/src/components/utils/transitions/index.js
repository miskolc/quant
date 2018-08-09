import CollapseTransition from './collapse-transition'
import './transition.less'
/* istanbul ignore next */
CollapseTransition.install = function (Vue) {
  Vue.component(CollapseTransition.name, CollapseTransition)
}

export default CollapseTransition
